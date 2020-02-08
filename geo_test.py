from geopy.geocoders import Nominatim  # convert an address into latitude and longitude values
from credentials import CLIENT_ID, CLIENT_SECRET
import os.path as path
import requests
import json
VERSION = '20180605'  # Foursquare API version


def foursquare_explore_venues(lat, lon, radius=500, limit=500):

    cache_key = "venues-explore_lat={}-lon={}-radius={}-limit={}".format(lat, lon, radius, limit)
    cache_file_name= "./data_tmp/" + cache_key + ".json"
    if path.exists(cache_file_name):
        with open(cache_file_name, 'r') as f:
            return  json.load(f)

    else:
        url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
            CLIENT_ID,
            CLIENT_SECRET,
            VERSION,
            lat,
            lon,
            radius,
            limit)
        print("cache miss for " , cache_key)
        r = requests.get(url)
        with open(cache_file_name, "wb") as f:
            f.write(r.content)

        with open(cache_file_name, 'r') as f:
            return  json.load(f)


def getNearbyVenues(names, latitudes, longitudes, radius=500, limit=500):
    venues_list = []
    for name, lat, lng in zip(names, latitudes, longitudes):
        print(name)
        results = foursquare_explore_venues(lat, lng, radius=radius, limit=limit)["response"]['groups'][0]['items']


        # return only relevant information for each nearby venue
        venues_list.append([(
            name,
            lat,
            lng,
            v['venue']['name'],
            v['venue']['location']['lat'],
            v['venue']['location']['lng'],
            v['venue']['categories'][0]['name']) for v in results])

    nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
    nearby_venues.columns = ['Neighborhood',
                             'Neighborhood Latitude',
                             'Neighborhood Longitude',
                             'Venue',
                             'Venue Latitude',
                             'Venue Longitude',
                             'Venue Category']

    return (nearby_venues)

b= 2
# address = 'New York City, NY'
# address = "Toronto"
# geolocator = Nominatim(user_agent="ny_explorer")
# location = geolocator.geocode(address)
# latitude = location.latitude
# longitude = location.longitude
# print('The geograpical coordinate of address are {}, {}.'.format(latitude, longitude))
#
manhattan_venues = getNearbyVenues(names=["fooo"],
                                   latitudes=[43.6542599],
                                   longitudes=[-79.3606359]
                                  )
