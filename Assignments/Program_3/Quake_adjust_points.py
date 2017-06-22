from dbscan import *
from Quake_file_helper import FileHelper


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


def mercX(lon):
    """
            Mercator projection from longitude to X coord
        Args:
            Float: longtudie
        Returns:
            Scaled X coordinates
        example:
            X = mercX(1000)
    """

    zoom = 1.0
    lon = math.radians(lon)
    a = (256.0 / math.pi) * pow(2.0, zoom)
    b = lon + math.pi
    return int(a * b)


def mercY(lat):
    """
            Mercator projection from latitude to Y coord
        Args:
            Float: latitude
        Returns:
            Int: scaled Y coordinates
        example:
            Y = mercY(1000)
    """

    zoom = 1.0
    lat = math.radians(lat)
    a = (256.0 / math.pi) * pow(2.0, zoom)
    b = math.tan(math.pi / 4 + lat / 2)
    c = math.pi - math.log(b)
    return int(a * c)


def adjust_location_coords(extremes, points, width, height):
    """
            Adjust points data to fit in the screen. 
        Args:
            Dictionary: extreme (x,y) values, Dictionary: points,
            Int: width of screen, Int: height of screen
        Returns:
            Dictionary with adjusted coordinates
            = {'1960':[(x,y),...,],'1961':[(x,y),...,],...,}
        example:
            Adjusted = adjust_location_coords({max_x: 1,...,}
                ,{'1960':[(x,y),...,],...,},1024,512)
            Adjusted now is a dictionary of scaled to the screen x, and y values
    """

    maxx = float(extremes['max_x'])
    minx = float(extremes['min_x'])
    maxy = float(extremes['max_y'])
    miny = float(extremes['min_y'])
    deltax = float(maxx) - float(minx)
    deltay = float(maxy) - float(miny)

    adjusted = {}

    for year in points.keys():
        adjusted[year] = []
        for i in range(len(points[year])):
            x, y = points[year][i]
            x = float(x)
            y = float(y)
            xprime = (x - minx) / deltax         # val (0,1)
            yprime = ((y - miny) / deltay)  # val (0,1)
            adjx = int(xprime * width)
            adjy = int(yprime * height)
            adjusted[year].append(tuple((adjx, adjy)))
    return adjusted


def convert_coordinates(dic, w, h, ep=25, m_p=15):
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
    points = {}
    allx = []
    ally = []
    for year in dic.keys():
        points[year] = []
        for i in range(len(dic[year])):
            lon = dic[year][i][0]
            lat = dic[year][i][1]
            x, y = (mercX(lon), mercY(lat))
            allx.append(x)
            ally.append(y)
            points[year].append((x, y))
     # Create dictionary to send to adjust method
    extremes = {}
    extremes['max_x'] = max(allx)
    extremes['min_x'] = min(allx)
    extremes['max_y'] = max(ally)
    extremes['min_y'] = min(ally)
    adjusted = adjust_location_coords(extremes, points, w, h)
    points = []
    for key in adjusted.keys():
        for point in adjusted[key]:
            points.append(tuple(point))
    adjusted['mbr'] = calculate_mbrs(points, ep, m_p)

    return adjusted


if __name__ == '__main__':

    pass
