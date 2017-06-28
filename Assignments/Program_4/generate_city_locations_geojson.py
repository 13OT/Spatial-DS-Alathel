
import json
import collections
import os
import sys


DIRPATH = os.path.abspath(os.path.dirname(__file__))


def cities_geojson(data, limit=None):

    feature_list = []

    for country, dict_list in data.items():

        for city in dict_list:
            properties = {}
            feature = collections.OrderedDict()

            for kk, ap in city.items():
                properties[kk] = ap

            lat = properties['lat']
            lon = properties['lon']
            del properties['lat']
            del properties['lon']
            feature["type"] = "Feature"
            feature["properties"] = properties
            feature["geometry"] = {"coordinates": [lon, lat],
                                   "type": "Point"}

            if len(feature_list) == limit:
                return feature_list

            feature_list.append(feature)

    return feature_list


PATH = os.path.abspath(
    os.path.join(DIRPATH, 'Json_Files', 'world_cities_large.json'))
f = open(PATH, 'r')
data = f.read()
f.close()
geo_json = cities_geojson(json.loads(data), 1000)
f = open(os.path.abspath(os.path.join(os.path.dirname(
    __file__), 'geo_json', 'world_cities.geojson')), "w")
f.write(json.dumps(geo_json, sort_keys=False, indent=2, separators=(',', ': ')))
f.close()
