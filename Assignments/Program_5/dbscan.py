from math import pow, sqrt
import math 

class Point(object):
    """
        Internal helper class to support algorithm implementation
     Attributes:
        __init__: initalize objects
        __str__: Returns points of a vector
     Usage:
        print(x)
    """
    def __init__(self,feature_vector):
        # feature vector should be something like a list or a numpy
        # array
        self.feature_vector = feature_vector
        self.cluster = None
        self.visited = False

    def __str__(self):
        return str(self.feature_vector)

def _as_points(points):
    """
            Convert a list of objects to internal Point class
        Args:
            List: points, 
        Returns:
            Dictionary: mbr[Cluster] = [(x,y),...,]
        example:
            points = _as_points(points)
    """
    return [Point(point) for point in points]

def as_lists(clusters):
    """
            Converts the Points in each cluster back into regular feature vectors 
        Args:
            Dictionary: points
        Returns:
            Dictionary: clusters_as_points[cluster] = [(x,y),...,]
        example:
            points = as_lists(points)
    """
    clusters_as_points = {}
    for cluster, members in clusters.items():
        clusters_as_points[cluster] = [member.feature_vector for member in members]
    return clusters_as_points



def euclidean(p0, p1):
    """
            Returns the euclidean of two points
        Args:
            Point: object, Point: object
        Returns:
            Float: euclidean
        example:
            Euclidean = euclidean(p0,p1)
    """
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def immediate_neighbours(point, all_points, epsilon, distance):
    """
            Find the immediate neighbours of a point.        
        Args:
            Point: object, List: of  points, Int: epsilon, Float: distance
        Returns:
            List: neighbouring points
        example:
            neighbours = immediate_neighbours(point, points, epsilon, distance)
    """
    neighbours = []
    for p in all_points:

        if p == point:
            continue
        d = distance(point.feature_vector,p.feature_vector)
        
        if d < epsilon:
            neighbours.append(p)

    return neighbours

def add_connected(points, all_points, epsilon, min_pts, current_cluster, distance):
    """
            Find every point in the set of all points which are
            density-connected, starting with the initial points list.        
        Args:
            List: points, List: of points, Int: epsilon, Int: min_pts, 
            Int: current_cluster, Float: distance
        Returns:
            List: connected points
        example:
            connected = add_connected(neighbours, points, epsilon, min_pts, current_cluster, distance)
    """
    cluster_points = []
    for point in points:

        if not point.visited:
            point.visited = True
            new_points = immediate_neighbours(point, all_points, epsilon, distance)

            if len(new_points) >= min_pts:                                
                for p in new_points:
                    if p not in points:
                        points.append(p)

        if not point.cluster:
            cluster_points.append(point)
            point.cluster = current_cluster

    return cluster_points

def dbscan(points, epsilon, min_pts, distance=euclidean):
    """
             Main dbscan algorithm function. pass in a list of feature
            vectors (most likely a list of lists or a list of arrays), a
            radius epsilon within which to search for neighbouring points, and
            a min_pts, the minimum number of neighbours a point must have
            within the radius epsilon to be considered connected. the default
            distance metric is euclidean, but another could be used as
            well. your custom distance metric must accept two equal-length
            feature vectors as input as return a distance value.      
        Args:
            List: points, Int: epsilon, Int: min_pts, Float: distance
        Returns:
            Dictionary: with clusters as keys (-1 are unclustered points)
        example:
            clusters = dbscan(points, epsilon, min_pts, distance)
    """
    assert isinstance(points, list)
    epsilon = float(epsilon)

    if not isinstance(points[0], Point):
        points = _as_points(points)
    
    clusters = {}     # each cluster is a list of points
    clusters[-1] = [] # store all the points deemed noise here. 
    current_cluster = -1

    for point in points:

        if not point.visited:
            point.visited = True
            neighbours = immediate_neighbours(point, points, epsilon, distance)

            if len(neighbours) >= min_pts:
                current_cluster += 1
                point.cluster = current_cluster                
                cluster = [point,]
                cluster.extend(add_connected(neighbours, points, epsilon, min_pts, 
                                             current_cluster, distance))
                clusters[current_cluster] = cluster

            else:
                clusters[-1].append(point)

    return as_lists(clusters)

if __name__ == '__main__':
    pass
