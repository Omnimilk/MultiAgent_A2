from ReadJson import FetchData
import numpy as np
from scipy.spatial.distance import euclidean,norm
from shapely.geometry import LineString, Polygon
from plots import plot_path,plot_map
import matplotlib.pylab as plt

def isFreeLine(startPoint,endPoint,obstacles):
    slope = np.subtract(endPoint,startPoint)*0.00001
    line = LineString([np.add(startPoint,slope),np.subtract(endPoint,slope)])
    for poly in obstacles:
        obstacle = Polygon(poly)
        if line.crosses(obstacle):
            return False
    return True

def getGraph(startPoint, endPoint, obstacles):
    """
    :param startPoint: starting point, 2-D tuple
    :param endPoint: end point, 2-D tuple
    :param obstacles: a list of polygons, each is a list of 2-D list points
    :return:a list of vertices and a distance matrix
    """
    vertices = [startPoint,endPoint]
    for polygon in obstacles:
        for ver in polygon:
            vertices.append(ver)
    size = len(vertices)
    graphEdges = np.zeros((size,size))
    # rs = pd.ix
    for i,ver in enumerate(vertices):
        for j, ver1 in enumerate(vertices):
            if isFreeLine(ver,ver1,obstacles):
                graphEdges[i][j] = euclidean(ver,ver1)
            else:
                graphEdges[i][j] = np.inf
    return (vertices,graphEdges)

def minDistance(s,distances):
    """
    :param  s: a set of points already in our path
            dist: a list of distances
    :return: index of the shortest distance in dist
    """
    smallestDistance = np.inf
    bestIndex = np.inf
    for i,dist in enumerate(distances):
        if i not in s:
            if dist <= smallestDistance:
                smallestDistance = dist
                bestIndex = i
    return bestIndex



def neighbors(vertexIndex,graph):
    neighborIndexes = []
    for i,dist in enumerate(graph[vertexIndex]):
        if 0<dist<np.inf:
            neighborIndexes.append(i)
    return neighborIndexes



def dijkstras(graph):
    """
    :param graph: a tuple contains a list of vertices and a edge matrix; first two vertices are start point and end point
    :return: the shortest path from start point to end point
    """
    vertices = graph[0]
    edges = graph[1]
    dist = np.full(len(vertices),np.inf)
    dist[0] = 0
    pred = [0]*len(vertices)
    s = set()
    Q = range(len(vertices))
    while len(Q)>0:
        u = minDistance(s,dist)
        Q.remove(u)
        s.add(u)
        for v in neighbors(u,edges):
            if dist[v]>dist[u] +edges[v][u]:
                dist[v] = dist[u]+edges[v][u]
                pred[v] = u
    path = distToPath(pred)
    pathPoints = []
    for i in path:
        pathPoints.append(vertices[i])
    return pathPoints

def distToPath(pred):
    p = 1 # end point index
    path = [p]
    while p != 0:#start point index
        p = pred[p]
        path.append(p)
    return path[::-1]

def VGshortest(data,startpoint,endpoint):
    obstables_and_boudary = data.allListPolygons
    graph = getGraph(startpoint,endpoint,obstables_and_boudary)
    path = dijkstras(graph)
    return path

def touchPoint(path,sensorRange):
    pathLen = euclidean(path[-2], path[-1])
    #is it possible that the end point is visible for points not in the last seg?
    if pathLen < sensorRange:
        return path[-2]
    dir = ((path[-2][0] - path[-1][0]) * sensorRange / pathLen, (path[-2][1] - path[-1][1]) * sensorRange / pathLen)
    return (dir[0] + path[-1][0], dir[1] + path[-1][1])


def calPathLength(path):
    lenth = 0
    for i in range(len(path)-1):
        lenth += euclidean(path[i],path[i+1])
    return lenth
#
# def monoTSPWithObstacles(data,startPoint,stations):
#     #construct the graph with matrix representation

def isInSight(map,station,item):
    polygons = map.obstacles_polygon
    sensor_range = map.sensor_range
    if euclidean(station,item)>sensor_range:
        return False
    line = LineString([station, item])
    for polygon in polygons:
        if line.crosses(polygon):
            return False
    return True



if __name__ == "__main__":
    data = FetchData('Problems/problem_A4.json')
    # obstables_and_boudary = data.allListPolygons
    # graph = getGraph((0,0),(15,15),obstables_and_boudary)
    # print(dijkstras(graph))
    plot_map(data)
    path = VGshortest(data,data.data['start_pos'],data.data["goal_pos2"])
    print(path)
    plot_path(path)
    plt.show()
