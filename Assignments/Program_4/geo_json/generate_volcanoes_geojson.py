
import json
import collections
import os,sys

#   {
#     "Altitude": "641",
#     "Country": "Honshu-Japan",
#     "Lat": "34.5",
#     "Lon": "131.6",
#     "Name": "Abu",
#     "Type": "Shield volcanoes"
#   },
def volcanoes_geojson(data,limit=None):
    feature_list = []
    geo_json = collections.OrderedDict()
    geo_json["type"] = "FeatureCollection"
    for volcano in data:
        properties = {}
        feature = collections.OrderedDict()
        for kk,ap in volcano.items():
            properties[kk] = ap
        lat = properties['Lat']
        lon = properties['Lon']
        del properties['Lat']
        del properties['Lon']
        feature["type"] = "Feature"
        feature["properties"] = properties
        feature["geometry"] = {"location": [lon, lat],"type":"Point"}
        if len(feature_list) == limit :
            return feature_list
        feature_list.append(feature)
    geo_json["features"] = feature_list
    return feature_list


DIRPATH = os.path.abspath(
    os.path.join('4553-Spatial-DS','Resources','Data','WorldData','world_volcanos.json'))

f = open(DIRPATH,'r')
data = f.read()
f.close()
geo_json = volcanoes_geojson(json.loads(data),1000)
f = open(os.path.abspath(os.path.join(os.path.dirname(__file__),'volcanoes.geojson')),"w")
f.write(json.dumps(geo_json, sort_keys=False,indent=2, separators=(',', ': ')))
f.close()