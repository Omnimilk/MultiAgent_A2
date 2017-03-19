from ReadJson import FetchData
from VGUtility import VGshortest,calPathLength,touchPoint
import collections
from pprint import pprint
from ant import ant_colony

def findMinimumTimeAgent(data,item):
    # return a list of costs for each agent
    shortestTimes = []
    minimum = float('inf')
    for i, startpos in enumerate(data.start_positions):
        path = VGshortest(data, startpos, item)
        dist = calPathLength(path)
        if dist > data.sensor_range:
            if dist < minimum:
                minimum = dist
                miniarg = i
                touchP = touchPoint(path,data.sensor_range)
        else:
            miniarg = i
        shortestTimes.append((dist-data.sensor_range)*1. / data.v_max)
    # return shortestTimes
    return shortestTimes, miniarg,touchP

def vote(map):
    costProfile = []
    voteTable = []
    responsibilityPartition = {}
    # construct cost profile matrix,N*D,N is the number of items, D is the number of agents
    for item in map.items:
        shortestTimes,miniarg,touchp = findMinimumTimeAgent(map,item)
        costProfile.append((shortestTimes,touchp))
        voteTable.append(miniarg)
    # construct the responsibilityPartition
    for i, agent in enumerate(map.start_positions):
        res = {j: map.items[j] for j, vote in enumerate(voteTable) if vote == i}
        #agent start position with -1 index
        st = {-1: agent}
        #merge agent with its responsibility
        dic = dict(st, **res)
        #each agent index with a value which is an ordered dict
        responsibilityPartition[i] = collections.OrderedDict(sorted(dic.iteritems(), key=lambda x: x[0]))
    pprint(responsibilityPartition)
    print(responsibilityPartition[1].get(10,"Not Found"))

    # do ant system for each agent on their responsibility
    def distance(start, end):
        return calPathLength(VGshortest(map, start, end))


    answers = []
    for key, responsibility in responsibilityPartition.items():
        colony = ant_colony(responsibility, distance)
        answer = colony.mainloop()
        print(key, answer)
        answers.append(answer)

def main():
    map = FetchData("Problems/problem_A4.json")
    vote(map)

if __name__ == "__main__":
    main()
