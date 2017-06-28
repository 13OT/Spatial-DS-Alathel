import json
import sys
import os
import collections


DIRPATH = os.path.abspath(os.path.dirname(__file__))


def airports_geojson(data, limit=None):

    feature_list = []

    for k, dict in data.items():
        properties = {}
        feature = collections.OrderedDict()

        for kk, ap in dict.items():
            properties[kk] = ap

        lat = properties['lat']
        lon = properties['lon']
        del properties['lat']
        del properties['lon']
        feature["type"] = "Feature"
        feature["properties"] = properties
        feature["geometry"] = {"coordinates": [lon, lat], "type": "Point"}

        if len(feature_list) == limit:
            return feature_list

        feature_list.append(feature)

    return feature_list


PATH = os.path.abspath(
    os.path.join(DIRPATH, 'Json_Files', 'airports.json'))
f = open(PATH, 'r')
data = f.read()
f.close()
geo_json = airports_geojson(json.loads(data), 1000)
f = open(os.path.abspath(os.path.join(os.path.dirname(
    __file__), 'geo_json', 'airports.geojson')), "w")
f.write(json.dumps(geo_json, sort_keys=False, indent=2, separators=(',', ': ')))
f.close()
