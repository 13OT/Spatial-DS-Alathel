

"""
Program:
--------
    Program 5 - Query Assignments - Query 1: Find Interesting Features along path:
    query1.py
Description:
------------
    This prgram reads in two points and a radius by entering airport codes via sys.argv 
    (e.g. python query1.py DFW MNL 1000 to run query from Dallas  to Manilla Philippines with a 1000 mile radius to look for interesting features).
    Highlight all features within R radius of the entire path by showing volcanos as red dots, earthquakes as blue dots, and meteor locations as green dots.
    
Name: Abdullah Alathel
Date: 05 July 2017
"""
import os
import sys
import math
import pygame
from pygame.locals import *
from pymongo import MongoClient
from map_icons import map_icon
from mongo_helper import MongoHelper
from map_helper import *
from color_helper import ColorHelper


mh = MongoHelper()
mf = MapFacade(2048, 1024)


def interesting_features(f, t, r):
    """
             draws path and interesting feature along the way from origin to destenation      
        Args:
            f: string, t: string, r: float
        Returns:
            None. Draws path on map
        example:
            interesting_features('DFW', 'RUH', 1000)
    """

    lines = []
    features = []
    volpoints = []
    eqpoints = []
    mpoints = []
    i = 0
    to = mh.get_airport_coord(t.upper())
    to_city=mh.get_airport_name(t.upper())
    loop = True
    from_ = mh.get_airport_coord(f.upper())
    lines.append(from_)
    while loop:
        distance = 9999999
        near = mh.get_airport_near_me(lines[i], float(r))
        x, y = to
        for ap in near:
            if ap['properties']['city'] == to_city:
                loop = False
            if ap['geometry']['coordinates'] in lines:
                continue
            x2, y2 = ap['geometry']['coordinates']
            d = mh._haversine(x, y, x2, y2)
            if d < distance:
                distance = d
                nearst = ap
        lines.append(nearst['geometry']['coordinates'])
        i = i + 1
    for p in lines:
        result = mh.get_features_near_me('meteorites', p, float(r))
        for rs in result:
            if rs not in mpoints:
                mpoints.append(
                    tuple((rs['geometry']['coordinates'][0], rs['geometry']['coordinates'][1])))
        result = mh.get_features_near_me('volcanoes', p, float(r))
        for rs in result:
            if rs not in volpoints:
                volpoints.append(
                    tuple((rs['geometry']['coordinates'][0], rs['geometry']['coordinates'][1])))
        result = mh.get_features_near_me('earthquakes', p, float(r))
        for rs in result:
            if rs not in eqpoints:
                eqpoints.append(
                    tuple((rs['geometry']['coordinates'][0], rs['geometry']['coordinates'][1])))
    adj = []
    for p in lines:
        a = mf.adjust_point(p)
        adj.append(a)
    mf.lines(adj)
    mf.pin_the_map(eqpoints, map_icon('Centered', 'Azure', 16, ''))
    mf.pin_the_map(volpoints, map_icon('Centered', 'Pink', 16, ''))
    mf.pin_the_map(mpoints, map_icon('Centered', 'Chartreuse', 16, ''))


interesting_features(sys.argv[1], sys.argv[2], sys.argv[3])
mf.draw_all_countries(1)
mf.run()
