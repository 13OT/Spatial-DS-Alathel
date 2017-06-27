# {
#   "AD": [
#     {
#       "city-name": "El Tarter",
#       "country-code": "AD",
#       "lat": "42.57952",
#       "lon": "1.65362",
#       "time-zone": "Europe/Andorra"
#     }
import json
import collections
import os,sys

def cities_geojson(data,limit=None):
    geo_json = collections.OrderedDict()
    geo_json["type"] = "FeatureCollection"
    feature_list = []
    for country,dict_list in data.items():
        for city in dict_list:
            properties = {}
            feature = collections.OrderedDict()
            for kk,ap in city.items():
                properties[kk] = ap
            lat = properties['lat']
            lon = properties['lon']
            del properties['lat']
            del properties['lon']
            feature["type"] = "Feature"
            feature["properties"] = properties
            feature["geometry"] = {"location": [lon, lat],
                "type":"Point"}
            if len(feature_list) == limit :
                return feature_list
            feature_list.append(feature)
    geo_json["features"] = feature_list
    return feature_list


DIRPATH = os.path.abspath(
    os.path.join('4553-Spatial-DS','Resources','Data','WorldData','world_cities_large.json'))
f = open(DIRPATH,'r')
data = f.read()
f.close()
geo_json = cities_geojson(json.loads(data),1000)
f = open(os.path.abspath(os.path.join(os.path.dirname(__file__),'world_cities.geojson')),"w")
f.write(json.dumps(geo_json, sort_keys=False,indent=2, separators=(',', ': ')))
f.close()