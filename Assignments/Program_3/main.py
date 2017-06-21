from Quake_adjust_points import *
from Quake_file_helper import *
import pygame
import os
import json
"""
    Program:
    --------
        Program 3 - Earth quakes

    Description:
    ------------
        This program reads earth quakes data from seperate .json files to, scale the points, and
        calculates MBR for each cluster of points, then prints them in .josn file named "Big_Quakes.json",
        and draws them on (1024 x 512) screen using pygame.

    Name: Abdullah Alathel
    Date: 22 June 2017
"""


# initialize variables

years = [x for x in range(1960, 2018)]
epsilon = 25
min_pts = 15
screen_width = 1024
screen_height = 512
background_colour = (255, 255, 255)
(width, height) = (1026, 514)
black = (0, 0, 0)

# get and convert coordinates

fh = FileHelper()
data = fh.get_data(years, 7)
adjusted = convert_coordinates(
    data, screen_width, screen_height, epsilon, min_pts)

# write file

f = open((os.path.dirname(__file__) + '\Big_Quakes.json'), 'w')
f.write(json.dumps(adjusted, sort_keys=False, indent=4, separators=(',', ': ')))
f.close()

# initialize pygame

pygame.init()
bg = pygame.image.load(os.path.dirname(
    __file__) + '\World_map.png')
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Quakes with magnitude of 7 or greater')
screen.fill(background_colour)
pygame.display.flip()

# main loop

running = True
while running:
    # background image
    screen.blit(bg, (0, 0))
    for id in adjusted.keys():
        # skip mbrs for now
        if id == 'mbr':
            continue
        for i in range(len(adjusted[id])):
            pygame.draw.circle(screen, (207, 83, 0), tuple(adjusted[id][i]), 2)
        # pygame.display.flip()
    for k in adjusted['mbr'].keys():
        # skip extremes and unclustered points
        if k == -1 or k == 'extremes':
            continue
        pygame.draw.polygon(screen, (159, 35, 35), adjusted['mbr'][k], 2)
    # save a screenshot
    pygame.image.save(screen, os.path.dirname(
        __file__) + '/Earthquakes.png')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
