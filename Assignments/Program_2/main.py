"""
    Program:
    --------
        Program 2 - Crimes in New York

    Description:
    ------------
        This program reads crime data from five files and plot them in (1000 x 1000) screen using pygame.
        dad are read into two dictionaries one sorts crimes based on location, other on type

    Name: Abdullah Alathel
    Date: 18 June 2017
"""
import pygame
import random
import json
import os

DIRPATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', '..', '4553-Spatial-DS', 'Resources'))


class Colors (object):
    """
           Opens a json file of web colors, and loads it into dictionary, to
        return an rgb of a random color or given one.
     Attributes:
        get_random_color: Returns a random rgb tuple from the color dictionary.
        get_rgb: Returns a named rgb tuple from the color dictionary.
    """

    def __init__(self, file_name=DIRPATH + '/Json_Files/colors.json'):
        """
        Opens a json file of web colors, and loads it into dictionary.
        """
        with open(file_name, 'r') as content_file:
            content = content_file.read()

        self.content = json.loads(content)

    def get_random_color(self):
        """
        Returns a random rgb tuple from the color dictionary
        Args:
            None
        Returns:
            color (tuple) : (r,g,b)
            example:

            c = Colors()
            some_color = c.get_random_color()

            some_color is now a tuple (r,g,b) representing some lucky color
        """
        r = random.randint(0, len(self.content) - 1)
        c = self.content[r]
        return (c['rgb'][0], c['rgb'][1], c['rgb'][2])

    def get_rgb(self, name):
        """
        Returns a named rgb tuple from the color dictionary
        Args:
            name (string) : name of color to return
        Returns:
            color (tuple) : (r,g,b)
        Usage:
            c = Colors()
            lavender = c.get_rgb('lavender')
            # lavender is now a tuple (230,230,250) representing that color
        """
        for c in self.content:
            if c['name'] == name:
                return (c['rgb'][0], c['rgb'][1], c['rgb'][2])
        return None


def scaled(crimes, width, height):
    """
        scales the x and y coordiantes in given dictionary, given width and height
        Args:
            dictionary, width, and height
        Returns:
            None
        Example:

            scaled(Dictionary,Width,Height)

            Dictionary now has the scaled coordinates
    """
    points = []
    for key in crimes.keys():
        points.extend(crimes[key]['location'])
    min_x = min(points)[0]
    max_x = max(points)[0]
    min_y = min(points)[1]
    max_y = max(points)[1]

    for key in crimes.keys():
        lst = []
        for i in crimes[key]['location']:
            x = int(width * ((i[0] - min_x) / ((max_x - min_x))))
            y = int(height * ((i[1] - min_y) / ((max_y - min_y))))
            y = -y + 915
            lst.append(tuple((x, y)))
        crimes[key]['location'] = lst


# intiliaize dictionary to store location by area
crimes_area = {}


def read_crimes():
    """
        Reads crime data from five different files with names in "crime_locations",
        Args:
            None
        Returns:
        Dictionary: crimes[Crime_Name] = {'location': [],
                        'color': A random color, 'mbrs': []}
        example:

            Dictionary = read_crimes()

            Dictionary in now a dictionary of crime names as keys
    """
    crimes = {}
    color = Colors()
    got_keys = False
    crime_locations = ['bronx', 'brooklyn',
                       'manhattan', 'queens', 'staten_island']
    crimes['random'] = {'location': [],
                        'color': color.get_random_color(), 'mbrs': []}

    for crime_place in crime_locations:
        crimes_area[crime_place] = {'location': [], 'color': None}
        with open(DIRPATH + '/NYPD_CrimeData/filtered_crimes_' + crime_place + '.csv') as f:
            for line in f:
                line = ''.join(x if i % 2 == 0 else x.replace(',', ':')
                               for i, x in enumerate(line.split('"')))
                line = line.strip().split(',')
                if not got_keys:
                    keys = line
                    got_keys = True
                    continue

                for e in line:
                    if e == '':
                        line.remove(e)
                try:

                    temp = int(line[7])
                    if line[9] not in crimes:
                        crimes[line[9]] = {
                            'location': [], 'color': color.get_random_color(), 'mbrs': []}
                    try:

                        crimes[line[9]]['location'].append(
                            tuple((float(line[-5]), float(line[-4]))))
                        crimes_area[crime_place]['location'].append(
                            tuple((float(line[-5]), float(line[-4]))))
                    except:
                        continue
                except:
                    if line[7] not in crimes:
                        crimes[line[7]] = {
                            'location': [], 'color': color.get_random_color(), 'mbrs': []}
                    try:
                        crimes[line[7]]['location'].append(
                            tuple((float(line[-5]), float(line[-4]))))
                        crimes_area[crime_place]['location'].append(
                            tuple((float(line[-5]), float(line[-4]))))
                    except:
                        continue
                try:
                    crimes['random']['location'].append(
                        tuple((float(line[-5]), float(line[-4]))))
                    crimes_area[crime_place]['location'].append(
                        tuple((float(line[-5]), float(line[-4]))))
                except:
                    continue
    return crimes


crimes = read_crimes()
scaled(crimes, 950, 515)
scaled(crimes_area, 950, 515)
crimes_area['manhattan']['color'] = (194, 35, 38)
crimes_area['queens']['color'] = (243, 115, 56)
crimes_area['staten_island']['color'] = (253, 182, 50)
crimes_area['brooklyn']['color'] = (128, 22, 56)
crimes_area['bronx']['color'] = (2, 120, 120)
(width, height) = (1000, 1000)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('New York Crimes')
screen.fill((255, 255, 255))
pygame.display.flip()
running = True
while running:
    for key in crimes_area.keys():
        for p in crimes_area[key]['location']:
            pygame.draw.circle(screen, crimes_area[key]['color'], p, 2, 0)
    pygame.image.save(screen, os.path.dirname(
        __file__) + '/all_buroughs_screen_shot.png')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
