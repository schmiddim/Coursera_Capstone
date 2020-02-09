from qwikidata.sparql import return_sparql_query_results


def get_entity_id_for_city_by_name(city_name):
    """

    :param city_name:
    :return: string Wikidata entity_id
    """
    sparql_query = """
    SELECT ?item ?itemLabel
    WHERE {{ 
        ?item wdt:P31/wdt:P279* wd:Q515 .
      ?item rdfs:label ?itemLabel. 
      FILTER(CONTAINS(LCASE(?itemLabel), "{}"@en)). 
    }} limit 1
    
    """.format(city_name.lower())
    res = return_sparql_query_results(sparql_query)
    url = res.get("results").get("bindings")[0].get('item').get('value')

    return url.replace('http://www.wikidata.org/entity/', '')


cities = [
    'Trier',
    'Saarbrücken',
    'Venedig',
    'Amsterdam',
    'Jerusalem',
    'Munich',
    'Bochum',
    'Essen',
    'New York',
    'Osaka',
    'LAS VEGAS',
    'Barcelona',
]

for city in cities:
    r = get_entity_id_for_city_by_name(city_name=city)
    print(city, r)

city = "Berlin"
r = get_entity_id_for_city_by_name(city_name=city)
print(r)
