
import json
import collections
import os
import sys


DIRPATH = os.path.abspath(os.path.dirname(__file__))


def states_geojson(data, limit=None):
    """
        Reads the state_borders.json file and and return it as geojson
        Args:
            Dictionary of a json file, and wanted list size
        Returns:
            A list of dictionaries of wanted size if given, or reads the whole file
        Usage:
             l = states_geojson(data) or = states_geojson(data,1000)
             l=[{},{},...,]
    """
    feature_list = []

    for state in data:
        properties = {}
        feature = collections.OrderedDict()

        for kk, ap in state.items():
            properties[kk] = ap

        geo = properties['borders']
        del properties['borders']
        feature["type"] = "Feature"
        feature["properties"] = properties
        feature["geometry"] = {"coordinates": geo, "type": "Polygon"}

        if len(feature_list) == limit:
            return feature_list

        feature_list.append(feature)

    return feature_list


PATH = os.path.abspath(
    os.path.join(DIRPATH, 'Json_Files', 'state_borders.json'))
f = open(PATH, 'r')
data = f.read()
f.close()
geo_json = states_geojson(json.loads(data), 1000)
f = open(os.path.abspath(os.path.join(os.path.dirname(
    __file__), 'geo_json', 'states.geojson')), "w")
f.write(json.dumps(geo_json, sort_keys=False, indent=2, separators=(',', ': ')))
f.close()
