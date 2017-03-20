from ReadJson import FetchData
from VGUtility import VGshortest,calPathLength,touchPoint
import collections
from pprint import pprint
from ant import ant_colony
from Simulation import Map

def findMinimumTimeAgent(data,item):
    # return a list of costs for each agent
    # shortestTimes = []
    minimum = float('inf')
    for i, startpos in enumerate(data.start_positions):
        path = VGshortest(data, startpos, item)
        dist = calPathLength(path)
        if dist > data.sensor_range:
            if dist < minimum:
                minimum = dist
                miniarg = i
                touchP = touchPoint(path,data.sensor_range)
                ST =(dist-data.sensor_range)*1. / data.v_max
        else:
            miniarg = i
        # shortestTimes.append((dist-data.sensor_range)*1. / data.v_max)
    # return shortestTimes
    return ST, miniarg,touchP

def vote(map):
    costProfile = []
    voteTable = []
    responsibilityPartition = {}
    # construct cost profile matrix,N*D,N is the number of items, D is the number of agents
    for item in map.items:
        shortestTimes,miniarg,touchp = findMinimumTimeAgent(map,item)
        costProfile.append((shortestTimes,touchp))
        voteTable.append((miniarg,shortestTimes,touchp))

    # construct the responsibilityPartition
    for i, agent in enumerate(map.start_positions):
        res = {j: vote for j, vote in enumerate(voteTable) if vote[0] == i}
        #each agent index with a value which is an ordered dict
        responsibilityPartition[i] = collections.OrderedDict(sorted(res.iteritems(), key=lambda x: x[1]))

    ans =[]
    for j,agent in enumerate(map.start_positions):
        part = [tuple(agent)]
        part.extend([tuple(x[2]) for _,x in responsibilityPartition[j].iteritems()])
        ans.append(part)
    pprint(ans)
    simumap = Map(map,ans)
    simumap.runGame()




def main():
    map = FetchData("Problems/problem_A4.json")
    vote(map)

if __name__ == "__main__":
    main()
