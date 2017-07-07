"""
Program:
--------
    Program 6 - Heat map.

Description:
------------
    Generate a heat style map showing terrorist hotspots around the world. by reading a json file of terrorism information, then display it using pygame
    
Name: Abdullah Alathel
Date: 7 July 2017
"""
import os
import sys
import math
import pygame
from pygame.locals import *
import json


class heat_map(object):
    """Reads data from json file to create a hate map of terrorism information.

    Attributes:
        read_data: reads the json file to extract coordinates and counts of terror
        get_radius: returns the radius of a circle based on given count
        get_width: returns the width of a circle based on given count
        get_color: returns the appropriate color for circle based on given count
        mercX: return the adjusted longitude
        mercY: returns the adjusted latitude
        run: creates a pygame instace to show the map and display the points
    """
    def __init__(self,width = 1024,height=512):
        """Inits SampleClass with width, and height."""
        self.width=width
        self.height = height
        self.coordinates = {}
        self.min = None
        self.max = None
        self.count = []
        self.DIRPATH = os.path.abspath(os.path.dirname(__file__))
        self.screen = None
        self.bg = None

    def read_data(self, data):
        """Reads the data and store it in dictionary"""
        x = []
        y = []
        for country, lst in data.items():
            for key, val in lst.items():
                self.coordinates[key] = {'count': val['count'], 'loc': tuple((self.mercX(
                    val['geometry']['coordinates'][0]), self.mercY(val['geometry']['coordinates'][1])))}
        for k in self.coordinates.keys():
            if self.coordinates[k]['count'] not in self.count:
                self.count.append(self.coordinates[k]['count'])
        self.max = max(self.count)
        self.min = min(self.count)


    def get_radius(self, x):
        """ returns radius based on given count"""
        return 27 * ((x - self.min) / (self.max - self.min)) + 1

    def get_width(self, x):
        """returns width based on given count"""
        return int(27 * ((x - self.min) / (self.max - self.min)) + 1)

    def get_color(self, count):
        """returns color based on given count"""
        EPSILON = sys.float_info.epsilon  # smallest possible difference
        minval, maxval = self.min, self.max
        steps = 26
        delta = float(maxval - minval) / steps
        colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]  # [BLUE, GREEN, RED]
        fi = float(count - minval) / float(maxval - minval) * (len(colors) - 1)
        i = int(fi)
        f = fi - i
        if f < EPSILON:
            return colors[i]
        else:
            (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i + 1]
            return int(r1 + f * (r2 - r1)), int(g1 + f * (g2 - g1)), int(b1 + f * (b2 - b1))

    def run(self):
        """creates and displays the map"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Terrorism Heat Map')
        self.bg = pygame.image.load(os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'map.png')))
        pygame.display.flip()
        running = True
        while running:
            self.screen.blit(self.bg, (0, 0))
            for k in self.coordinates.keys():
                pygame.draw.circle(self.screen, self.get_color(self.coordinates[k]['count']), self.coordinates[k]['loc'], int(
                    self.get_radius(self.coordinates[k]['count'])), self.get_width(self.coordinates[k]['count']))
            pygame.display.flip()
            pygame.image.save(self.screen, os.path.dirname( __file__) + '/screen_shot.png')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()

    def mercX(self, lon, zoom=1):
        """returns the adjusted longitude"""
        lon = math.radians(lon)
        a = 256 / math.pi * pow(2, zoom)
        b = lon + math.pi
        return int((((a * b) / 1024) * 1024))

    def mercY(self, lat, zoom=1):
        """returns the adjusted latitude"""
        lat = math.radians(lat)
        a = 256.0 / math.pi * pow(2, zoom)
        b = math.tan(math.pi / 4 + lat / 2)
        c = math.pi - math.log(b)
        return int(((a * c) / 512 * 512 - (512 / 2)))

f = open(os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'attacks.json')), 'r')
file = f.read()
map = heat_map()
map.read_data(json.loads(file))
map.run()
f.close()
