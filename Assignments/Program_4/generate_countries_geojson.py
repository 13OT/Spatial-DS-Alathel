
import json
import sys
import os
import collections


DIRPATH = os.path.abspath(os.path.dirname(__file__))


def countries_geojson(data, limit=None):
    """
        Reads the countries.geo.json file and and return it as geojson
        Args:
            Dictionary of a json file, and wanted list size
        Returns:
            A list of dictionaries of wanted size if given, or reads the whole file
        Usage:
             l = countries_geojson(data) or = countries_geojson(data,1000)
             l=[{},{},...,]
    """
    feature_list = []

    for dict in data['features']:
        properties = {}
        properties["id"] = dict["id"]
        properties["name"] = dict["properties"]["name"]
        feature = collections.OrderedDict()
        feature["type"] = "Feature"
        feature["properties"] = properties
        feature["geometry"] = {"coordinates": dict["geometry"]
                               ["coordinates"], "type": dict["geometry"]["type"]}

        if len(feature_list) == limit:
            return feature_list

        feature_list.append(feature)

    return feature_list


PATH = os.path.abspath(
    os.path.join(DIRPATH, 'Json_Files', 'countries.geo.json'))
f = open(PATH, 'r')
data = f.read()
f.close()
geo_json = countries_geojson(json.loads(data), 1000)
f = open(os.path.abspath(os.path.join(os.path.dirname(
    __file__), 'geo_json', 'countries.geojson')), "w")
f.write(json.dumps(geo_json, sort_keys=False, indent=2, separators=(',', ': ')))
f.close()
