from pymongo import MongoClient
import pprint as pp
from math import radians, cos, sin, asin, sqrt
import os,sys


class mongoHelper(object):
    def __init__(self):
        self.client = MongoClient()

        self.db_airports = self.client.geo.airports
        self.db_states = self.client.geo.states
        self.db_ap = self.client.world_data.airports
        self.db_earthquakes = self.client.world_data.earthquakes
        self.db_volcanoes = self.client.world_data.volcanoes
        self.db_cities = self.client.world_data.cities
        self.db_state = self.client.world_data.states
        self.db_countries = self.client.world_data.countries

        



    def get_airports_in_poly(self,poly):
        """
        Get airports within some polygon
        Params:
            poly (object): geojson poly
        """
        state_airports = self.db_airports.find( { 'loc' : { '$geoWithin' : { '$geometry' : poly } } })

        ap_list = []
        for ap in state_airports:
            ap_list.append(ap)

        return ap_list

    def get_state_poly(self,state):
        state_poly = self.db_states.find_one({'code' : state})
        return(state_poly['loc'])

    def get_afb_airports(self):

        
        res = self.db_airports.find({"type" : "Military"})

        res_list = []
        for r in res:
            res_list.append(r)

        return res_list

    def get_doc_by_keyword(self,db_name,field,key):
        if db_name == 'airports':
            res = self.db_airports.find({field : {'$regex' : ".*"+key+".*"}})
        else:
            res = self.states.find({field : {'$regex' : ".*"+key+".*"}})
        
        res_list = []
        for r in res:
            res_list.append(r)

        return res_list

    def get_nearest_neighbor(self,lon,lat,r):
       # air_res = self.db_ap.find( { 'geometry' : { '$geoWithin' : { '$geometry' : poly } } })
        air_res = self.db_ap.find( { 'geometry': { '$geoWithin': { '$centerSphere': [ [lon, lat ] , r / 3963.2 ] } }} )

        min = 999999
        
        for ap in air_res:
            lon2 = ap['geometry']['coordinates'][0]
            lat2 = ap['geometry']['coordinates'][1]
            d = self._haversine(lon,lat,lon2,lat2)
            if d < min:
                min = d
                print(d)
                print(ap['properties']['name'])
                closest_ap = ap

        return closest_ap

    def get_state_by_point(self,point):
        return self.db_states.find_one({'loc':{'$geoIntersects':{'$geometry':{ "type" : "Point","coordinates" : point }}}})

    def get_state_by_name(self,name):
        pass

    def _haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 3956 # Radius of earth in kilometers. Use 6371 for km
        return c * r


def main():
    mh = mongoHelper()
    poly = mh.get_state_poly("CA")
    ap = mh.get_airports_in_poly(poly)
    afb = mh.get_afb_airports()
    f = open(os.path.abspath(os.path.join(os.path.dirname(
    __file__), 'mongo_out.txt')), "w")
    bykey = mh.get_doc_by_keyword('airports','name','County')

    pp.pprint(bykey,f)

    state = mh.get_state_by_point([-95.912512, 41.118327])
    pp.pprint(state,f)
    f.write(str(mh.get_nearest_neighbor(11.513672, 53.018914 ,100)))

    f.close()


if __name__=='__main__':
    main()