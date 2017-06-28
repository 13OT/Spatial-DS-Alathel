
import json
import collections
import os
import sys


DIRPATH = os.path.abspath(os.path.dirname(__file__))


def volcanoes_geojson(data, limit=None):
    """
        Reads the world_vlocanos.json file and and return it as geojson
        Args:
            Dictionary of a json file, and wanted list size
        Returns:
            A list of dictionaries of wanted size if given, or reads the whole file
        Usage:
             l = volcanoes_geojson(data) or = volcanoes_geojson(data,1000)
             l=[{},{},...,]
    """

    feature_list = []

    for volcano in data:
        properties = {}
        feature = collections.OrderedDict()

        for kk, ap in volcano.items():
            properties[kk] = ap

        lat = properties['Lat']
        lon = properties['Lon']
        del properties['Lat']
        del properties['Lon']
        feature["type"] = "Feature"
        feature["properties"] = properties
        feature["geometry"] = {"coordinates": [lon, lat], "type": "Point"}

        if len(feature_list) == limit:
            return feature_list

        feature_list.append(feature)

    return feature_list


PATH = os.path.abspath(
    os.path.join(DIRPATH, 'Json_Files', 'world_volcanos.json'))
f = open(PATH, 'r')
data = f.read()
f.close()
geo_json = volcanoes_geojson(json.loads(data), 1000)
f = open(os.path.abspath(os.path.join(os.path.dirname(
    __file__), 'geo_json', 'volcanoes.geojson')), "w")
f.write(json.dumps(geo_json, sort_keys=False, indent=2, separators=(',', ': ')))
f.close()
