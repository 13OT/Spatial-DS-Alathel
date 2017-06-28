
import json
import collections
import os
import sys


DIRPATH = os.path.abspath(os.path.dirname(__file__))


def earthquakes_geojson(data, limit=None):

    feature_list = []

    for year, dict_list in data.items():

        for quake in dict_list:
            properties = {}
            properties["year"] = year
            feature = collections.OrderedDict()

            for kk, ap in quake.items():

                if kk != "geometry":
                    properties[kk] = ap

            feature["type"] = "Feature"
            feature["properties"] = properties
            feature["geometry"] = quake["geometry"]

            if len(feature_list) == limit:
                return feature_list

            feature_list.append(feature)

    return feature_list


PATH = os.path.abspath(
    os.path.join(DIRPATH, 'Json_Files', 'earthquakes-1960-2017.json'))
f = open(PATH, 'r')
data = f.read()
f.close()
geo_json = earthquakes_geojson(json.loads(data),1000)
f = open(os.path.abspath(os.path.join(
    os.path.dirname(__file__),'geo_json', 'earthquakes.geojson')), "w")
f.write(json.dumps(geo_json, sort_keys=False, indent=2, separators=(',', ': ')))
f.close()
