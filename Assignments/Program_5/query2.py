"""
Program:
--------
    Program 5 - Query Assignments - Query 2: Nearest Neighbor
    query2.py
Description:
------------
    This program will find features with a radius of a location, location can be inputed as a Click on the world map, or read from sys.argv, 
    further filtering the queries is possible, where features are listed below:
        Volcanos
        Earthquakes
        Meteors
    Example queries may be:
        python query2.py [feature] [field] [field value] [min/max] [max results] [radius] [lon,lat]
            feature = volcano, earthquake, meteor
            field = some field in the 'properties' to compare against
            field_value = the value in wich to compare with
            min/max = whether we want all results greater than or less than the field_value.
            radius (in miles) = radius to apply our query with.
            lon,lat (optional) = Some point coords to act as a mouse click instead of actually clicking the screen.
    python query2.py volcanos altitude 3000 min 3 1000 
    When the map is clicked it will find the 3 volcanos within a 1000 mile radius that are at a minumum of 3000 feet (if they exist at that location).
    python query2.py earthquakes magnitude 5 min 0 2000 
    When the map is clicked it will find ALL earthquakes (max results 0 = all) within a 2000 mile radius with a magnitude of 5 or more.
    python query2.py 1000 
    This query if run with a single parameter, it will assume it is a Radius and will find ALL of the above features within that radius
    (Volcanos, Earthquakes, Meteors). 
    It will show volcanos as red dots, earthquakes as blue dots, and meteor locations as green dots.
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


class PygameHelper(object):
    def __init__(self, width, height):
        self.screen_width = width
        self.screen_height = height
        self.keyval = 1000
        self.mh = MongoHelper()
        self.bg = pygame.image.load(os.path.join(BASE, "images/2048x1024.png"))

        self.polygons = []             # any polygon to be drawn
        self.polygon = []                # clusters' mbrs
        self.points = []               # any point to be drawn
        self.lines = []
        self.map_event_functions = {}

        pygame.init()
        self.game_images = {}

    def Capture(self, name, pos, size):  # (pygame Surface, String, tuple, tuple)
        image = pygame.Surface(size)  # Create image surface
        # Blit portion of the display to the image
        image.blit(self.screen, (0, 0), (pos, size))
        pygame.image.save(image, name)  # Save the image to the disk

    def load_image(self, key, path, coord):
        """
        Params:
            key: name to reference image with
            path: path to image 
            coord: location to place image on screen
        """
        self.game_images[key] = {
            'pyg_image': pygame.image.load(path), 'coord': coord}

    def adjust_point(self, p, icon=None):
        if icon:
            size = self._get_icon_size(icon)
            voffset = size
            hoffset = size // 2
        else:
            voffset = 0
            hoffset = 0

        lon, lat = p
        x = (mercX(lon) / 1024 * self.screen_width) - hoffset
        scale = 1 / math.cos(math.radians(lat))             # not used
        y = (mercY(lat) / 512 * self.screen_height) - \
            (self.screen_height / 2) - voffset
        return (x, y)

    def add_polygon(self, polygon, color, width):
        """
        Add polygons to local list to be drawn
        """
        outofrange = [-180, -90, -99, 180, 90]
        adjusted = []
        for p in polygon[0]:
            if math.floor(p[0]) in outofrange or p[1] in outofrange:
                continue
            adjusted.append(self.adjust_point(p))
        self.polygons.append(
            {'poly': adjusted, 'color': color, 'width': width})

    def add_points(self, point, icon):
        """
        Add points to local list to be drawn
        """
        if type(point) is list:
            for p in point:
                coord = self.adjust_point(p, icon)
                self.load_image(self._unique_key(), icon, coord)

    def draw_polygons(self):
        for poly in self.polygons:
            if len(poly['poly']) < 3:
                continue
            pygame.draw.polygon(
                self.screen, poly['color'], poly['poly'], poly['width'])

    def start_display(self, args=None):
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.screen.blit(pygame.transform.scale(
            self.bg, (self.screen_width, self.screen_height)), (0, 0))

        for key, image in self.game_images.items():
            self.screen.blit(image['pyg_image'], image['coord'])
        pygame.display.flip()
        while True:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    if args:
                        point = toLL(event.pos, self.screen_width,
                                     self.screen_height)
                        wait_loc(args, point)

                        for key, image in self.game_images.items():
                            self.screen.blit(
                                image['pyg_image'], image['coord'])
                    pygame.display.flip()
                    pygame.image.save(self.screen,  'screen_shot.png')
                if event.type == KEYUP:
                    if event.key == 273:
                        pass
                    if event.key == 274:
                        pass
                if event.type == QUIT:
                    pygame.display.quit()

            self.draw_polygons()
            pygame.display.flip()

    def _unique_key(self):
        key = self.keyval
        self.keyval += 1
        return key

    def _get_icon_size(self, icon):
        sizes = ['16x', '32x', '64x', '128x']
        for size in sizes:
            if size in icon:
                return int(size.replace('x', ''))


def nearest_neighbors(feature, field, value, min_max, max_results, radius, lon_lat):
    """
            Finds a specific feature in a radius      
        Args:
            feature: string, field: string, value: float, min_max:string, max_results:int, radius:float, lon_lat:tuple
        Returns:
            None. Draws path on map
        example:
            nearest_neighbors(volcanoes, altitude, 3000, max, 0, 1000, (0,0))
    """
    icon = map_icon('Centered', 'Azure', 16, '')
    fields = ['mag', 'Altitude']
    if field.strip(" ").lower() == 'magnitude':
        field = fields[0]
    if field.strip(" ").lower() == 'altitude':
        field = fields[1]
    if feature.strip(" ").lower() == 'volcanos':
        feature = 'volcanoes'
    if isinstance(lon_lat, str):
        temp = lon_lat.split(',')
        lon_lat = tuple(
            (float(temp[0].replace('(', '')), float(temp[1].replace(')', ''))))
    res = mh.get_features_near(
        feature, lon_lat, field, float(value), min_max, float(radius))
    points = []
    for i in res:
        points.append(
            tuple((i['geometry']['coordinates'][0], i['geometry']['coordinates'][1])))
    if int(max_results) == 0 or len(res) <= int(max_results):
        mf.pin_the_map(points, icon)
    else:
        limited = []
        for i in range(int(max_results)):
            limited.append(points[i])
        mf.pin_the_map(limited, icon)


def get_all(radius, point):
    """
            Finds all features in a radius      
        Args:
            radius: float, point: tuple
        Returns:
            None. Draws path on map
        example:
            get_all(5000,(0,0))
    """
    
    features = ['volcanoes', 'earthquakes', 'meteorites']
    res = {}
    points = {}
    icons = {}
    icons['volcanoes'] = map_icon('Centered', 'Pink', 16, '')
    icons['earthquakes'] = map_icon('Centered', 'Azure', 16, '')
    icons['meteorites'] = map_icon('Centered', 'Chartreuse', 16, '')
    for f in features:
        res[f] = mh.get_features_near_me(f, point, float(radius))
    for k in res.keys():
        points[k] = []
        for i in res[k]:
            points[k].append(
                tuple((i['geometry']['coordinates'][0], i['geometry']['coordinates'][1])))
    for k in points.keys():
        mf.pin_the_map(points[k], icons[k])


def wait_loc(args, point):
    if len(args) > 2:
        nearest_neighbors(args[1], args[2], args[3],
                          args[4], args[5], args[6], point)
    else:
        get_all(args[1], point)


def find_features(args):
    if len(args) == 8:
        nearest_neighbors(args[1], args[2], args[3],
                          args[4], args[5], args[6], args[7])
        mf.run()
    else:
        mf.run(args)


screen_width = 2048
screen_height = 1024
pyg = PygameHelper(screen_width, screen_height)
mh = MongoHelper()
mf = MapFacade(screen_width, screen_height, pyg)
mf.draw_all_countries(1)
find_features(sys.argv)
