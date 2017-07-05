
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
from dbscan import *


mh = MongoHelper()
mf = MapFacade(2048, 1024)


def calculate_mbrs(points, epsilon, min_pts):
    """
            Call dbscan to find clusters, then calculated the mbr for each cluster
        Args:
            List: all the points, Int: minimum distance between points, 
            Int: minimum points to consider a cluster
        Returns:
            Dictionary: mbr[Cluster] = [(x,y),...,]
        example:
            Mbr = calculate_mbrs([(x,y),...,],25,10)
            Mbr in now a dictionary of minimum bounding rectangles with clusters as keys
    """
    mbrs = {}
    clusters = dbscan(points, epsilon, min_pts)
    extremes = {'max_x': 100000 * -1, 'max_y': 100000 * -
                1, 'min_x': 100000, 'min_y': 100000}

    for id, cpoints in clusters.items():
        xs = []
        ys = []
        for p in cpoints:
            xs.append(p[0])
            ys.append(p[1])
        max_x = max(xs)
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)

        if max_x > extremes['max_x']:
            extremes['max_x'] = max_x
        if max_y > extremes['max_y']:
            extremes['max_y'] = max_y
        if min_x < extremes['min_x']:
            extremes['min_x'] = min_x
        if min_y < extremes['min_y']:
            extremes['min_y'] = min_y

        mbrs[id] = [(min_x, min_y), (max_x, min_y),
                    (max_x, max_y), (min_x, max_y), (min_x, min_y)]
    mbrs['extremes'] = extremes
    return mbrs


def find_clusters(feature, m_p=15, ep=25, limit=None):
    """
            Loop through read points to convert coordinates using mercX,
            and mercY on each pair
            call adjust_location_coords to scale the converted coordinates
            calculate mbrs for the clusters
        Args:
            Dictionary: points to be converted, Int: width of screen, 
            Int: height of screen
        Returns:
            Dictionary with adjusted coordinates
            {'1960':[(x,y),...,],'1961':[(x,y),...,],...,
                'mbr':{'-1':[(x,y),...,],...,}
        example:
            Adjusted = convert_coordinates(data,screen_width,screen_height)
            Adjusted now is a dictionary of scaled to the screen x, and y values

    """
    if limit == None:
        limit = 5000
    else:
        limit = int(limit)
    if feature.lower() == 'all':
        feature = ['volcanoes', 'earthquakes', 'meteorites']
    icons = {}
    icons['volcanoes'] = map_icon('Centered', 'Pink', 16, '')
    icons['earthquakes'] = map_icon('Centered', 'Azure', 16, '')
    icons['meteorites'] = map_icon('Centered', 'Chartreuse', 16, '')
    m_p = int(m_p)
    ep = int(ep)
    adj_mbrs = {}
    points = {}
    adj = {}
    mbrs = {}
    features_list = {}
    allx = []
    ally = []
    if isinstance(feature, str):
        features_list[feature] = mh.get_all(feature)
    else:
        for i in feature:
            features_list[i] = mh.get_all(i)
    for k, lst in features_list.items():
        points[k] = []
        for f in lst:
            lon = f["geometry"]["coordinates"][0]
            lat = f["geometry"]["coordinates"][1]
            if int(lon) == 0 and int(lat) == 0:
                continue
            try:
                points[k].append((float(lon), float(lat)))
            except:
                continue

    for k, l in points.items():
        adj[k] = []
        for p in l:
            a = mf.adjust_point(p)
            if len(adj[k]) > limit:
                break
            adj[k].append(a)
    for k in adj.keys():
        mbrs[k] = calculate_mbrs(adj[k], ep, m_p)
    for key in mbrs.keys():
        adj_mbrs[key] = []
        for k in mbrs[key].keys():
            # skip extremes and unclustered points
            if k == -1 or k == 'extremes':
                continue
            if len(adj_mbrs[key]) >= 3:
                break
            adj_mbrs[key].append(mbrs[key][k])
    for k in points.keys():
        mf.pin_the_map(points[k], icons[k])
    for k in adj_mbrs.keys():
        mf.mbrs(adj_mbrs[k])


mf.draw_all_countries(1)
if len(sys.argv) == 4:
    find_clusters(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    find_clusters(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
mf.run()
