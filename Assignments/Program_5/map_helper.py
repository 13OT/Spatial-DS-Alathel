import os
import sys
import math
import pygame
from pygame.locals import *
from pymongo import MongoClient
from map_icons import map_icon
from mongo_helper import MongoHelper
from color_helper import ColorHelper
BASE = os.path.dirname(os.path.realpath(__file__))

def get_extremes(points):
    maxX = -999
    minX = 999
    maxY = -999
    minY = 999


def merc_xy(lon, lat):
    r_major = 6378137.0
    x = r_major * math.radians(lon)
    if lat > 89.5:
        lat = 89.5
    if lat < -89.5:
        lat = -89.5
    r_major = 6378137.0
    r_minor = 6356752.3142
    temp = r_minor / r_major
    eccent = math.sqrt(1 - temp ** 2)
    phi = math.radians(lat)
    sinphi = math.sin(phi)
    con = eccent * sinphi
    com = eccent / 2
    con = ((1.0 - con) / (1.0 + con)) ** com
    ts = math.tan((math.pi / 2 - phi) / 2) / con
    y = 0 - r_major * math.log(ts)
    return (
     x, y)


def mercXY(lon, lat):
    r = 6378137
    scale = math.cos(lat * math.pi / 180.0)
    x = scale * lon * math.pi * r / 180.0
    y = scale * r * math.log(math.tan((90.0 + lat) * math.pi / 360.0))
    return (
     x, y)


def mercX(lon, zoom=1):
    lon = math.radians(lon)
    a = 256 / math.pi * pow(2, zoom)
    b = lon + math.pi
    return a * b


def mercY(lat, zoom=1):
    lat = math.radians(lat)
    a = 256.0 / math.pi * pow(2, zoom)
    b = math.tan(math.pi / 4 + lat / 2)
    c = math.pi - math.log(b)
    return a * c


def mercToLL(point):
    lng, lat = point
    lng = lng / 256.0 * 360.0 - 180
    n = math.pi - 2.0 * math.pi * lat / 256.0
    lat = 180.0 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n)))
    return (
     lng, lat)


def toLL(point,width,height):
    x, y = point
    x = x / width * height
    y = (y + (height/2)) / height * (height/2)
    return mercToLL((x / 4, y / 4))


def adjust_location_coords(extremes, points, width, height):
    """
    Adjust your point data to fit in the screen.
    Input:
        extremes: dictionary with all maxes and mins
        points: list of points
        width: width of screen to plot to
        height: height of screen to plot to
    """
    maxX = float(extremes['maxX'])
    minX = float(extremes['minX'])
    maxY = float(extremes['maxY'])
    minY = float(extremes['minY'])
    deltax = float(maxX) - float(minX)
    deltay = float(maxY) - float(minY)
    adjusted = []
    for p in points:
        x, y = p
        x = float(x)
        y = float(y)
        xprime = (x - minX) / deltax
        yprime = (y - minY) / deltay
        adjx = int(xprime * width)
        adjy = int(yprime * height)
        adjusted.append((adjx, adjy))

    return adjusted


def flatten_country_polygons(geometry):
    adjusted_polys = []
    if geometry['type'] == 'Polygon':
        pass
    else:
        for polygons in geometry['coordinates']:
            for polygon in polygons:
                newp = []
                for p in polygon:
                    newp.append([mercX(p[0]), mercY(p[1])])

                adjusted_polys.append(newp)

        return adjusted_polys


class PygameHelper(object):

    def __init__(self, width, height):
        self.screen_width = width
        self.screen_height = height
        self.keyval = 1000
        self.mh = MongoHelper()
        self.bg = pygame.image.load(os.path.join(BASE, 'images/2048x1024.png'))
        self.polygons = []
        self.polygon = []
        self.points = []
        self.lines = []
        self.map_event_functions = {}
        pygame.init()
        self.game_images = {}

    def Capture(self, name, pos, size):
        image = pygame.Surface(size)
        image.blit(self.screen, (0, 0), (pos, size))
        pygame.image.save(image, name)

    def load_image(self, key, path, coord):
        """
        Params:
            key: name to reference image with
            path: path to image
            coord: location to place image on screen
        """
        self.game_images[key] = {'pyg_image':pygame.image.load(path),
         'coord':coord}

    def adjust_point(self, p, icon = None):
        if icon:
            size = self._get_icon_size(icon)
            voffset = size
            hoffset = size // 2
        else:
            voffset = 0
            hoffset = 0
        lon, lat = p
        x = mercX(lon) / 1024 * self.screen_width - hoffset
        scale = 1 / math.cos(math.radians(lat))
        y = mercY(lat) / 512 * self.screen_height - self.screen_height / 2 - voffset
        return (
         x, y)

    def add_polygon(self, polygon, color, width):
        """
        Add polygons to local list to be drawn
        """
        outofrange = [
         -180, -90, -99, 180, 90]
        adjusted = []
        for p in polygon[0]:
            if not math.floor(p[0]) in outofrange:
                if p[1] in outofrange:
                    continue
                    adjusted.append(self.adjust_point(p))

        self.polygons.append({'poly':adjusted, 'color':color, 'width':width})

    def add_points(self, point, icon):
        """
        Add points to local list to be drawn
        """
        if type(point) is list:
            for p in point:
                coord = self.adjust_point(p, icon)
                self.load_image(self._unique_key(), icon, coord)

        else:
            self.load_image(self._unique_key(), icon, point)

    def draw_polygon(self, polys):
        for poly in polys:
            self.polygon.append(poly)

    def draw_lines(self, points):
        self.lines.extend(points)

    def draw_polygons(self):
        for poly in self.polygons:
            if len(poly['poly']) < 3:
                continue
                pygame.draw.polygon(self.screen, poly['color'], poly['poly'], poly['width'])

    def get_all(self, radius, point):
        features = [
         'volcanoes', 'earthquakes', 'metoerites']
        res = []
        points = []
        icon = map_icon('Centered', 'Azure', 32, '')
        for f in features:
            res.extend(self.mh.get_features_near_me(f, point, float(radius)))

        for i in res:
            points.append(tuple((i['geometry']['coordinates'][0], i['geometry']['coordinates'][1])))

        self.add_points(points, icon)

    def wait_loc(self, args, point):
        if len(args) > 2:
            self.nearest_neighbor(args[1], args[2], args[3], args[4], args[5], args[6], point)
        else:
            self.get_all(args[1], point)

    def nearest_neighbor(self, feature, field, value, min_max, max_results, radius, lon_lat):
        icon = map_icon('Centered', 'Azure', 32, '')
        fields = ['mag', 'Altitude']
        if field.strip(' ').lower() == 'magnitude':
            field = fields[0]
        if field.strip(' ').lower() == 'altitude':
            field = fields[1]
        if feature.strip(' ').lower() == 'volcanos':
            feature = 'volcanoes'
        res = self.mh.get_features_near(feature, lon_lat, field, float(value), min_max, float(radius))
        points = []
        for i in res:
            points.append(tuple((i['geometry']['coordinates'][0], i['geometry']['coordinates'][1])))

        if int(max_results) == 0 or len(res) <= int(max_results):
            self.add_points(points, icon)
        else:
            limited = []
            for i in range(int(max_results)):
                limited.append(points[i])

            self.add_points(limited, icon)

    def start_display(self):
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.screen.blit(pygame.transform.scale(self.bg, (self.screen_width, self.screen_height)), (0,
                                                                                                    0))
        for key, image in self.game_images.items():
            self.screen.blit(image['pyg_image'], image['coord'])

        if self.lines:
            pygame.draw.lines(self.screen, (255, 255, 255), False, self.lines, 2)

        if self.polygon:
            for poly in self.polygon:
                pygame.draw.polygon(self.screen, (159, 35, 35), poly, 2)

        pygame.display.flip()
        while True:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    pygame.display.flip()
                    pygame.image.save(self.screen, 'screen_shot3.png')
                if event.type == KEYUP:
                    if event.key == 273:
                        if event.key == 274:
                            if event.type == QUIT:
                                pygame.display.quit()

            self.draw_polygons()
            pygame.display.flip()
    def _unique_key(self):
        key = self.keyval
        self.keyval += 1
        return key

    def _get_icon_size(self, icon):
        sizes = [
         '16x', '32x', '64x', '128x']
        for size in sizes:
            if size in icon:
                return int(size.replace('x', ''))


class MapFacade(object):

    def __init__(self, width, height, pyg=None):
        self.screen_width = width
        self.screen_height = height
        self.mh = MongoHelper()
        if pyg is None:
            self.pyg = PygameHelper(width, height)
        else:
            self.pyg = pyg

    def run(self, args = None):
        if args is None:
            self.pyg.start_display()
        else:
            self.pyg.start_display(args)

    def draw_country(self, codes, color, width):
        for code in codes:
            country = self.mh.get_country_poly(code)
            if country is not None:
                break

        if country['type'] == 'MultiPolygon':
            for polygon in country['coordinates']:
                self.pyg.add_polygon(polygon, color, width)

        else:
            self.pyg.add_polygon(country['coordinates'], color, width)

    def draw_airports(self, icon):
        airports = self.mh.get_all('airports')
        points = []
        for ap in airports:
            points.append(ap['geometry']['coordinates'])

        self.pyg.add_points(points, icon)

    def pin_the_map(self, points, icon):
        self.pyg.add_points(points, icon)

    def lines(self, points):
        self.pyg.draw_lines(points)

    def mbrs(self, polys):
        self.pyg.draw_polygon(polys)

    def circles(self, points):
        pass

    def adjust_point(self, point, icon=None):
        return self.pyg.adjust_point(point, icon)

    def draw_all_countries(self, border):
        c = ColorHelper()

        countries = self.mh.get_all('countries', {}, {'_id':0, 'properties.MAPCOLOR13':1, 'properties.ISO_A3':1, 'properties.ADM0_A3_US':1, 'properties.SU_A3':1, 'properties.GU_A3':1})
        for country in countries:
            codes = []
            color = int(country['properties']['MAPCOLOR13']) - 1
            for c in ('ISO_A3', 'ADM0_A3_US', 'SU_A3', 'GU_A3'):
                if not str(c) == '-99':
                    codes.append(country['properties'][c])

            if color < 0:
                color = 13
            self.draw_country(codes, (255,255,255), border)