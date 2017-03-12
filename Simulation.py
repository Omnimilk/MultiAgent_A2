import pygame
from pprint import pprint
from pygame.locals import *
from ReadJson import FetchData
from VGUtility import isInSight
from scipy.spatial.distance import euclidean
import numpy as np
from numpy.linalg import norm

FPS = 24
WINWIDTH = 1100
WINHEIGHT = 750
RED = (255,0,0)
WHITE = (255,255,255)
BLUE = (0,128,255)
BLACK = (0,0,0)
LINEWIDTH = 3



class Agent(pygame.sprite.Sprite):
    def __init__(self,agentPos,radius):
        pygame.sprite.Sprite.__init__(self)
        self.pos = agentPos
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        # self.rect.center = self._pointCoordinationTransformation(agentPos)
        self.rect.center = agentPos
        self.sensor_range = radius

    def update(self,newPos):
        self.rect.center = newPos

class Item(pygame.sprite.Sprite):
    def __init__(self,pos,width =5,height=5,color=WHITE):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # self.rect.center = self._pointCoordinationTransformation(pos)
        self.rect.center = pos

class Map(object):
    def __init__(self,data,pathMatrix):
        self.data = data
        self.speed = data.v_max
        self.scaleForMap = 30
        self.xOffset = 180
        self.yOffset = 25
        self.n = 0
        # self.pathIsReady = False
        self.pathMatrix = pathMatrix
        self._constructObjGroups()
        pygame.init()
        self.FPSCLOCK = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    def _polygonCoordinationTransformation(self,polygon_list):
        return [(point[0]*self.scaleForMap+self.xOffset,point[1]*self.scaleForMap+self.yOffset) for point in polygon_list]

    def _pointCoordinationTransformation(self,point):
        return (point[0] * self.scaleForMap + self.xOffset, point[1] * self.scaleForMap + self.yOffset)

    def _constructObjGroups(self):
        self.unseenItemGroup = pygame.sprite.Group()
        for item in self.data.items:
            itemObj = Item(item)
            itemObj.add(self.unseenItemGroup)
            item = self._pointCoordinationTransformation(item)
            itemObj.rect.center = item
        # self.agentsGroup = pygame.sprite.Group()
        self.agentsGroup = []
        for agent in self.data.start_positions:
            agentObj = Agent(agent, self.data.sensor_range)
            # print(agent)
            # agentObj.add(self.agentsGroup)
            agent = self._pointCoordinationTransformation(agent)
            agentObj.rect.center = agent
            self.agentsGroup.append(agentObj)


    def updateUnseenItems(self):
        for item in self.unseenItemGroup.sprites():
            for agent in self.agentsGroup:
                # print("agent",len(self.unseenItemGroup))
                # if isInSight(self.data,agent.rect.center,item.rect.center):
                if euclidean(agent.pos,item.pos)<=self.data.sensor_range:
                    self.unseenItemGroup.remove(item)
                    break
                    # item.kill()

    def executePath(self,ticks):
        #each row in the path for each agent
        for i,agent in enumerate(self.agentsGroup):
            path = self.pathMatrix[i]
            self._executeSinglePath(agent,path,ticks)
            # for point in path[1:]:
            #     self._executeSegment(agent,point,ticks)

    def _executeSinglePath(self,agent,path,ticks):
        if not path:
            done = True
            return done
        if path:
            done = False
            doneThisPoint = self._executeSegment(agent,path[0],ticks)
            if doneThisPoint:
                path.pop(0)
            return done



    def _executeSegment(self,agent,goal,ticks):
        #goal in regular map scale
        rgDir = (goal[0]-agent.pos[0],goal[1]-agent.pos[1])
        goal = self._pointCoordinationTransformation(goal)
        dir = (goal[0]-agent.rect.center[0],goal[1]-agent.rect.center[1])
        lenth = norm(dir)
        time = 1000*lenth/(self.speed*self.scaleForMap)
        # print("time",time)
        if time>40:
            agent.rect.center = (agent.rect.center[0]+float(ticks/time)*dir[0],agent.rect.center[1]+float(ticks/time)*dir[1])
            agent.pos = (agent.pos[0] + float(ticks / time) * rgDir[0], agent.pos[1] + float(ticks / time) * rgDir[1])
            done = False
            return done
        else:
            done = True
            return done


    def _drawMap(self,ticks):
        # draw the map
        # draw the boundary
        self.screen.fill(BLACK)
        boundary = self._polygonCoordinationTransformation(self.data.boundary_polygon_list)
        pygame.draw.polygon(self.screen, BLUE, boundary, LINEWIDTH)

        # draw obstacles
        for polygon in self.data.obstacles_list:
            polygon = self._polygonCoordinationTransformation(polygon)
            pygame.draw.polygon(self.screen, BLUE, polygon, LINEWIDTH)

        # draw agents
        # self._executeSegment(self.agentsGroup.sprites()[0],(5,10),ticks)
        self.executePath(ticks)
        for agent in self.agentsGroup:
            pygame.draw.circle(self.screen, RED, agent.rect.center, 20,
                               LINEWIDTH)
            pygame.draw.circle(self.screen, WHITE, agent.rect.center, self.data.sensor_range * self.scaleForMap,LINEWIDTH)

        # draw items
        self.updateUnseenItems()
        for itemObj in self.unseenItemGroup:
            pygame.draw.rect(self.screen, RED, itemObj, LINEWIDTH)



    def runGame(self):
        done = False
        ticks = 0
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            self._drawMap(ticks)
            pygame.display.update()
            ticks = self.FPSCLOCK.tick(FPS)

def readAndConvert():
    rs = []
    with open("Problems/log.txt") as f:
        for line in f:
            # line.strip()
            # print(line, type(line))
            if line =="NEW PATH\r\n":
                newpath = []
                rs.append(newpath)
            else:
                x,y = line.split(",")
                newpath.append((-float(x)/100.,float(y)/100))
    return rs

def mapPathToAgent(pathMatrix,map):
    agents = map.start_positions
    rs = []
    for agent in agents:
        for path in pathMatrix:
            if abs(path[0][0]-agent[0])<0.1 and abs(path[0][1]-agent[1])<0.1:
                rs.append(path[1:])
                break
    return rs
# def convert(rsMatrix):
#     newM = []
#     for path in rsMatrix:
#         newPath = []
#         for point in path[1:len(path)-1]:
#             newPath.append((-point[0]/100.,point[1]/100.))
#         newM.append(newPath)
#     return newM

def main():
    data = FetchData("Problems/problem_A12.json")
#     rsMatrix = [
#         [
#             (-2010.0, 2110.0),
#             (-1922.050659, 2190.629883),
#             (-292.258636, 1326.390747),
#             (-1768.590698, 1787.649536),
#             (-292.258636, 1326.390747),
#             (-1865.642334, 1539.400024),
#             (-292.258636, 1326.390747),
#             (-1578.56189, 1542.690796),
#             (-292.258636, 1326.390747),
#             (-1524.643677, 1153.356934),
#             (-292.258636, 1326.390747),
#             (-1750.900879, 1093.01355),
#             (-292.258636, 1326.390747),
#             (-1796.998291, 873.422058),
#             (-292.258636, 1326.390747),
#             (-1807.51001, 549.735168),
#             (-292.258636, 1326.390747),
#             (-1419.694946, 556.715759),
#             (-292.258636, 1326.390747)
#         ],
#         [
#             (-209.999985, 410.0),
#             (-30.23242, 21.181656),
#             (-292.258636, 1326.390747),
#             (-363.223846, 110.380661),
#             (-292.258636, 1326.390747),
#             (-823.885132, 113.740433),
#             (-292.258636, 1326.390747),
#             (-851.959351, 409.973175),
#             (-292.258636, 1326.390747),
#             (-1252.425171, 102.964058),
#             (-292.258636, 1326.390747),
#             (-1828.818115, 90.327461),
#             (-292.258636, 1326.390747)
#         ],
#         [
#             (-1210.0, 1410.0),
#             (-1060.146973, 996.93158),
#             (-292.258636, 1326.390747),
#             (-970.449524, 1794.052002),
#             (-292.258636, 1326.390747),
#             (-703.874146, 1917.814087),
#             (-292.258636, 1326.390747),
#             (-743.002563, 1596.772217),
#             (-292.258636, 1326.390747),
#             (-1309.510498, 2082.224854),
#             (-292.258636, 1326.390747)
#         ],
#         [
#             (-209.999985,1410.0),
#             (-292.258636,1326.390747),
#             (-292.258636,1326.390747),
#             (-251.920898,1137.342529),
#             (-292.258636,1326.390747),
#             (-212.436356,741.225952),
#             (-292.258636,1326.390747),
#             (-459.3703,730.927063),
#             (-292.258636,1326.390747),
#             (-562.766907,988.128418),
#             (-292.258636,1326.390747),
#             (-207.219635,1747.03772),
#             (-292.258636,1326.390747),
#             (-113.921196,1995.93811),
#             (-292.258636,1326.390747)
#         ]
# ]
#     rsMatrix = convert(rsMatrix)
    rsMatrix = readAndConvert()
    rsMatrix = mapPathToAgent(rsMatrix,data)
    pprint(rsMatrix)
    map = Map(data,rsMatrix)
    map.runGame()

if __name__ == "__main__":
    main()
