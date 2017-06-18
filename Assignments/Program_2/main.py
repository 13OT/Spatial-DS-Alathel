import pygame
import random
import json

def calculate_mbrs(points, epsilon, min_pts):
    """
    Find clusters using DBscan and then create a list of bounding rectangles
    to return.
    """
    print("CLUSTERS< AHHHHHHHHHHHHHHHHHHHHHHH")
    mbrs = []
    #clusters = dbscan(points, epsilon, min_pts)

    print("DONE WITH SCANS, calculating mbrs")

    """
    Traditional dictionary iteration to populate mbr list
    Does same as below
    """
    # for id,cpoints in clusters.items():
    #     xs = []
    #     ys = []
    #     for p in cpoints:
    #         xs.append(p[0])
    #         ys.append(p[1])
    #     max_x = max(xs)
    #     max_y = max(ys)
    #     min_x = min(xs)
    #     min_y = min(ys)
    #     mbrs.append([(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y),(min_x,min_y)])
    # return mbrs

    """
    Using list index value to iterate over the clusters dictionary
    Does same as above
    """



def clean_area(screen,origin,width,height,color):
    """
    Prints a color rectangle (typically white) to "erase" an area on the screen.
    Could be used to erase a small area, or the entire screen.
    """
    ox,oy = origin
    points = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    pygame.draw.polygon(screen, color, points, 0)
class Colors ( object ):
    """
    Opens a json file of web colors.
    """

    def __init__(self, file_name='C:/Users/Aalat/Documents/4553-Spatial-DS/Resources/Json_Files/colors.json'):

        with open ( file_name, 'r' ) as content_file:
            content = content_file.read ()

        self.content = json.loads ( content )

    def get_random_color(self):
        """
        Returns a random rgb tuple from the color dictionary
        Args:
            None
        Returns:
            color (tuple) : (r,g,b)
        Usage:
            c = Colors()
            some_color = c.get_random_color()
            # some_color is now a tuple (r,g,b) representing some lucky color
        """
        r = random.randint ( 0, len ( self.content ) - 1 )
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

    def __getitem__(self, color_name):
        """
        Overloads "[]" brackets for this class so we can treat it like a dict.
        Usage:
            c = Colors()
            current_color = c['violet']
            # current_color contains: (238,130,238)
        """
        return self.get_rgb ( color_name )

def scaled(crimes):
    points=[]
    for key in crimes.keys ():
        points.extend ( crimes[key]['location'] )
    min_x = min ( points )[0]
    max_x = max ( points )[0]
    min_y = min ( points )[1]
    max_y = max ( points )[1]
    for key in crimes.keys ():
        lst = []
        for i in crimes[key]['location']:
            x = int(950*((i[0]-min_x)/((max_x-min_x))))
            y = int ( 515*((i[1] - min_y) / ((max_y - min_y))) )
            lst.append(tuple((x,y)))
        crimes[key]['location']=lst
# Get current working path
DIRPATH = 'C:/Users/Aalat/Documents/4553-Spatial-DS/Resources/NYPD_CrimeData/'
color = Colors ()
keys = []
crimes = {}
crimes['random']={'location': [], 'color': color.get_random_color (), 'mbrs': []}
got_keys = False
crime_locations=['bronx','brooklyn','manhattan','queens','staten_island']
for crime_place in crime_locations:
    with open ( DIRPATH + 'filtered_crimes_'+crime_place+'.csv' ) as f:
        for line in f:
            line = ''.join ( x if i % 2 == 0 else x.replace ( ',', ':' ) for i, x in enumerate ( line.split ( '"' ) ) )
            line = line.strip ().split ( ',' )
            if not got_keys:
                keys = line
                print ( keys )
                got_keys = True
                continue

            for e in line:
                if e =='':
                    line.remove(e)
            if isinstance(line[7],str):
                if line[7] not in crimes:
                    crimes[line[7]] = {'location': [], 'color': color.get_random_color (), 'mbrs': []}
                try:
                    crimes[line[7]]['location'].append ( tuple ( (float(line[-5]),float(line[-4]))))
                except:
                    continue
            try:
                crimes['random']['location'].append ( tuple ( (float ( line[-5] ), float ( line[-4] )) ) )
            except:
                continue
scaled(crimes)
background_colour = (255, 255, 255)
black = (0, 0, 0)
(width, height) = (1024, 900)
screen = pygame.display.set_mode ( (width, height) )
pygame.display.set_caption ( 'New York Crimes' )
screen.fill ( background_colour )
pygame.display.flip ()
running = True
while running:
    for key in crimes.keys():
        for p in crimes[key]['location']:
            pygame.draw.circle ( screen, crimes[key]['color'], p, 2, 0 )
    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clean_area ( screen, (0, 0), width, height, (255, 255, 255) )
    pygame.display.flip ()
