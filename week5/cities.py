from qwikidata.linked_data_interface import get_entity_dict_from_api
import pandas as pd
from wikidata.client import Client
import os.path

class WikiDataWrapper:
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.entity = get_entity_dict_from_api(entity_id)

    def get_name(self):
        return self.entity.get('labels').get("en").get("value")

    def get_image_from_entity_dict(self):
        """
        Returns url to the full image path
        @see https://stackoverflow.com/a/34402875
        :return:
        """
        client = Client()
        entity = client.get(self.entity_id, load=True)

        image_prop = client.get("P18")
        image = entity[image_prop]
        return image.image_url

    def get_coordinate_location(self):
        """
        :return: lat, lon
        """
        property = self.entity.get("claims").get("P625")[0].get('mainsnak').get('datavalue').get('value')
        return property.get('latitude'), property.get('longitude')

    def get_population(self):
        """
        https://www.wikidata.org/wiki/Property:P1082 population
        :return:
        """
        property = self.entity.get("claims").get("P1082")[-1].get('mainsnak').get('datavalue').get('value').get(
            "amount")
        return int(property)

    def get_area(self):
        """
        https://www.wikidata.org/wiki/Property:P2046 area 415,9 m^2
        :return:
        """
        property = self.entity.get("claims").get("P2046")[-1].get('mainsnak').get('datavalue').get('value').get(
            "amount")
        return float(property)

    def get_population_density(self):
        return self.get_population() / self.get_area()

    def get_boroughs(self):
        """

        Venice Q641 has  6 boroughs
            - Cannaregio (including San Michele),
            - San Polo,
            - Dorsoduro (including Giudecca and Sacca Fisola),
            - Santa Croce,
            - San Marco (including San Giorgio Maggiore) and
            - Castello (including San Pietro di Castello and Sant'Elena).
         https://www.wikidata.org/wiki/Property:P150        contains administrative territorial entity
        :return:
        """
        bourough_ids = []
        bouroughs = []

        property = self.entity.get("claims").get("P150")
        # @Todo Q_TRIER = "Q3138" has NO P150
        if property is None:

            print(self.entity_id, "has no P150")
            lat, lon = self.get_coordinate_location()
            bouroughs.append({"Name": self.get_name(), "Lat": lat, "Lon": lon})
            return bouroughs


        for item in property:
            entity = item.get("mainsnak").get("datavalue").get('value').get('id')
            bourough_ids.append(entity)

        for entity_id in bourough_ids:
            entity = get_entity_dict_from_api(entity_id)
            english_label = entity.get('labels').get("en")
            if None is english_label:
                key = next(iter(entity.get('labels')))
                bourough_name = entity.get('labels').get(key).get("value")
            else:
                bourough_name = entity.get('labels').get("en").get("value")
            property = entity.get("claims").get("P625")[0].get('mainsnak').get('datavalue').get('value')
            lat, lon = property.get('latitude'), property.get('longitude')

            bouroughs.append({"Name": bourough_name, "Lat": lat, "Lon": lon})

        return bouroughs

    def get_series_for_data_frame(self):
        lat, lon = self.get_coordinate_location()
        return {'Name': self.get_name(),
                "EntityID": self.entity_id,
                'Population': self.get_population(),
                'Area': self.get_area(),
                'PopulationDensity': self.get_population_density(),
                'Lat': lat,
                'Lon': lon,
                'Image': self.get_image_from_entity_dict(),
                "Bouroughs": self.get_boroughs()
                }



cities = ["Q3138", "Q1724",  "Q1726",   "Q1492", "Q727", "Q1218", "Q2103", "Q2066", "Q60", "Q35765",
          "Q23768"]
df_cities = pd.DataFrame()

# wrapper = WikiDataWrapper(Q_VENICE)
# s = wrapper.get_image_from_entity_dict()
# +print(s)

path_name = "cities_with_wikidata.json"

if not os.path.exists(path_name):
    print("Cache miss")
    for city in cities:
        wrapper = WikiDataWrapper(city)
        df_cities = df_cities.append(wrapper.get_series_for_data_frame(), ignore_index=True)

    df_cities.to_json(path_or_buf=path_name)
with open(path_name, 'r') as f:
    df_cities = pd.read_json(path_name)

print(df_cities)



# area = wrapper.get_area()
# population = wrapper.get_population()
# lat, lon = wrapper.get_coordinate_location()
# img = (wrapper.get_image_from_entity_dict())
# density = wrapper.get_population_density()
# print(wrapper.get_name())
