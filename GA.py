import itertools
import numpy as np
import random
from ReadJson import FetchData

class GA(object):
    def __init__(self,stations,agents,stopCondition=None):
        self.stations = stations
        self.agents = agents
        self.ns = len(stations)
        self.na = len(agents)
        self.stopCondition = stopCondition


    def _generateLegalAssignment(self):
        randomAssignment = []
        leftStations = self.ns
        for i in xrange(self.na):
            if i ==self.na-1:
                randomAssignment.append(leftStations)
                break
            ran = random.randint(0,leftStations)
            leftStations -= ran
            randomAssignment.append(ran)
        return randomAssignment

    def chromosomeFromStations(self):
        #use a two-part representation of chromosome:[cities;number of cities for each agent]
        for permu in itertools.permutations(self.stations):
            yield permu.extend(self._generateLegalAssignment())

    def calChromosomeFitness(self):
        pass


if __name__ == '__main__':
    stations = [[17.45732746979441, 2.4064179342623815], [4.428480104257616, 9.677822446966168], [17.323213996844547, 10.193549584656221], [7.798954326057114, 17.748915791901496], [17.06017952936315, 18.48176897105862], [11.056000713738403, 3.7880960383671534], [2.670367230273758, 13.95308113348487], [2.1005039595379955, 3.846397475922742], [6.658964806672953, 1.2458886798354742], [10.624353001594155, 13.072017054583958], [11.923147183147696, 20.98449420634846], [17.205915991191695, 14.016178171845743], [15.143054701349472, 6.369553988470927], [1.3073899148332282, 17.61590756722544], [2.4533888345304264, 9.936419912958568], [4.974725221720545, 7.923803991835397], [13.077536588924906, 1.4424399324803618], [19.549304013183, 22.084236210439567], [6.480963623687236, 18.060437352893455], [14.476557812119408, 13.026148338126266], [10.473014624902325, 7.362274602051394], [18.58461450530498, 4.597937336575091], [17.248732720786812, 16.610848006861918], [1.3816342692596546, 0.8629709425936725], [2.122364653687683, 7.890726794325859], [6.85367665146313, 13.484502091802588], [6.728685566304234, 6.872029648585112], [17.603787873346047, 21.01373403518971], [8.082666415235794, 19.946592883378667], [18.234896398328583, 0.3743317238554041], [17.09493856471422, 7.561405750342837]]
    data = FetchData('Problems/problem_A12.json')
    agents = data.start_positions
    ga = GA(stations,agents)
    print(list(ga._generateStationPermutation()))
    # print(ga.chromosomeFromStations())
