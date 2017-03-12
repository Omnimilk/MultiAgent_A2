from ReadJson import FetchData
from plots import  plot_map
from plots import plot_cover_range
import matplotlib.pylab as plt
import numpy as np
from shapely.geometry import Point,LineString
from scipy.spatial.distance import euclidean
from VGUtility import VGshortest,calPathLength,isInSight# data,start,end
# from random import sample
import collections
# from scipy.spatial import ConvexHull
from copy import copy
# from ant import ant_colony

def positioning_Guards(data,N,triesForSingleStation):
    stations = []
    items = copy(data.items)
    items = collections.OrderedDict.fromkeys(items)
    sensor_range = data.sensor_range
    totalCovered = 0
    for i in range(N):
        tries = triesForSingleStation
        maxCovered = 0
        maxStation =[]
        while True:
            if not tries:
                break
            x = np.random.uniform(low=data.approximatedBoundary[0], high=data.approximatedBoundary[2])
            y = np.random.uniform(low=data.approximatedBoundary[1], high=data.approximatedBoundary[3])

            # #do not get too close to the boundary, a bit arbitrary now
            # x = np.random.uniform(low=data.approximatedBoundary[0]+sensor_range/2., high=data.approximatedBoundary[2]-sensor_range/2.)
            # y = np.random.uniform(low=data.approximatedBoundary[1]+sensor_range/2., high=data.approximatedBoundary[3]-sensor_range/2.)

            pos = Point(x, y)
            isFreeState = True
            # check if it is in the boundary
            if not data.boundary_polygon_polygon.contains(pos):
                isFreeState = False
            # check if it is out of the obstacles
            if isFreeState:
                for poly in data.obstacles_polygon:
                    if poly.contains(pos):
                        isFreeState = False

            # # do not get to too close to existing stations
            # if stations and isFreeState:
            #     for station in stations:
            #         #a bit arbitrary about how close is too close now
            #         if euclidean(station,[x,y])<sensor_range:
            #             isFreeState=False

            if isFreeState:
                tries -=1
                #count how many items can this new station cover
                cover_count = 0
                for item in items:
                    # if euclidean(item,[x,y])<= sensor_range:
                    if isInSight(data,[x,y],item):
                        cover_count +=1
                        # items.remove(item)
                if cover_count>maxCovered:
                    maxCovered = cover_count
                    maxStation = [x,y]
        if maxStation:
            stations.append(maxStation)
        for item in items:
            if isInSight(data,maxStation,item):
                del items[item]
        totalCovered += maxCovered
    return stations,totalCovered

def findWholeCoverSets(data):
    total = len(data.items)
    BestSets =[]
    for i in range(30,36):#depends on map
        stations,totalcovered = positioning_Guards(data,i,40)
        if totalcovered==total:
            BestSets = stations
            break
    return BestSets

def shortRangeSearch(data):
    # stations = findWholeCoverSets(data)
    # print(stations)
    stations = [[17.45732746979441, 2.4064179342623815], [4.428480104257616, 9.677822446966168], [17.323213996844547, 10.193549584656221], [7.798954326057114, 17.748915791901496], [17.06017952936315, 18.48176897105862], [11.056000713738403, 3.7880960383671534], [2.670367230273758, 13.95308113348487], [2.1005039595379955, 3.846397475922742], [6.658964806672953, 1.2458886798354742], [10.624353001594155, 13.072017054583958], [11.923147183147696, 20.98449420634846], [17.205915991191695, 14.016178171845743], [15.143054701349472, 6.369553988470927], [1.3073899148332282, 17.61590756722544], [2.4533888345304264, 9.936419912958568], [4.974725221720545, 7.923803991835397], [13.077536588924906, 1.4424399324803618], [19.549304013183, 22.084236210439567], [6.480963623687236, 18.060437352893455], [14.476557812119408, 13.026148338126266], [10.473014624902325, 7.362274602051394], [18.58461450530498, 4.597937336575091], [17.248732720786812, 16.610848006861918], [1.3816342692596546, 0.8629709425936725], [2.122364653687683, 7.890726794325859], [6.85367665146313, 13.484502091802588], [6.728685566304234, 6.872029648585112], [17.603787873346047, 21.01373403518971], [8.082666415235794, 19.946592883378667], [18.234896398328583, 0.3743317238554041], [17.09493856471422, 7.561405750342837]]
    agents = data.start_positions
    #Use GA to solve this problem as a MTSP problem



def minimumTimeToStation(data,station):
    #return a list of costs for each agent
    shortestTimes = []
    minimum = float('inf')
    for i,startpos in enumerate(data.start_positions):
        path = VGshortest(data,startpos,station)
        dist = calPathLength(path)
        if dist>data.sensor_range:
            if dist < minimum:
                minimum = dist
                miniarg = i
        else:
            miniarg = i
        shortestTimes.append(dist/data.v_max)
    # return shortestTimes
    return shortestTimes,miniarg







if __name__ == "__main__":
    data = FetchData("Problems/problem_A12.json")
    shortRangeSearch(data)


