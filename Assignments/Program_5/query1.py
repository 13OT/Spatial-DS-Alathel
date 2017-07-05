
import os,sys
import math
import pygame
from pygame.locals import *
from pymongo import MongoClient
from map_icons import map_icon
from mongo_helper import MongoHelper
from map_helper import *
from color_helper import ColorHelper


mh = MongoHelper()
mf = MapFacade(2048,1024)

def interesting_features(f,t,r):

    lines=[]
    features=[]
    volpoints=[]
    eqpoints=[]
    mpoints=[]
    i = 0
    to = mh.get_airport_coord(t.upper())
    loop = True
    from_ = mh.get_airport_coord(f.upper())
    lines.append(from_)
    while loop:
        distance = 9999999
        near = mh.get_airport_near_me(lines[i],float(r))
        x,y = to
        for ap in near:
            if ap ['geometry']['coordinates'] == to:
                loop = False
            if ap['geometry']['coordinates'] in lines:
                continue
            x2,y2 = ap['geometry']['coordinates']
            d = mh._haversine(x,y,x2,y2)
            if d < distance:
                distance =d
                nearst = ap
        lines.append(nearst['geometry']['coordinates'])
        i = i+1
    for p in lines:
        result=mh.get_features_near_me('meteorites',p,float(r))
        for rs in result:
            if rs not in mpoints:
                mpoints.append(tuple((rs['geometry']['coordinates'][0],rs['geometry']['coordinates'][1])))            
        result=mh.get_features_near_me('volcanoes',p,float(r))
        for rs in result:
            if rs not in volpoints:
                volpoints.append(tuple((rs['geometry']['coordinates'][0],rs['geometry']['coordinates'][1])))            
        result=mh.get_features_near_me('earthquakes',p,float(r))
        for rs in result:
            if rs not in eqpoints:
                eqpoints.append(tuple((rs['geometry']['coordinates'][0],rs['geometry']['coordinates'][1])))            
    adj=[]
    for p in lines:
        a=mf.adjust_point(p)
        adj.append(a)
    mf.lines(adj)
    mf.pin_the_map(eqpoints, map_icon('Centered','Azure',16,''))
    mf.pin_the_map(volpoints, map_icon('Centered','Pink',16,''))
    mf.pin_the_map(mpoints, map_icon('Centered','Chartreuse',16,''))

interesting_features(sys.argv[1],sys.argv[2],sys.argv[3])
mf.draw_all_countries(1)
mf.run()