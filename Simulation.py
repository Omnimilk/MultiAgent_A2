import pygame
from pprint import pprint
from pygame.locals import *
from ReadJson import FetchData
from VGUtility import isInSight
from scipy.spatial.distance import euclidean
import numpy as np
from copy import deepcopy
from numpy.linalg import norm

FPS = 50
WINWIDTH = 1100
WINHEIGHT = 900
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
        # self.scaleForMap = 30
        # self.xOffset = 180
        # self.yOffset = 25
        self.xOffset = 180
        self.yOffset = 25
        self.scaleForMap = int(min((WINWIDTH-self.xOffset*2)/(self.data.approximatedBoundary[2]-self.data.approximatedBoundary[0]),\
                                   (WINHEIGHT-self.yOffset*2)/(self.data.approximatedBoundary[2]-self.data.approximatedBoundary[0]))\
                               -1)
        self.pathCopy = deepcopy(pathMatrix)
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
                if isInSight(self.data,agent.pos,item.pos):
                # if euclidean(agent.pos,item.pos)<=self.data.sensor_range:
                    self.unseenItemGroup.remove(item)
                    break
                    # item.kill()

    def executePath(self,ticks):
        #each row in the path for each agent
        for i,agent in enumerate(self.agentsGroup):
            path = self.pathMatrix[i]
            self._executeSinglePath(agent,path,ticks)

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
        if time>50:
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
                # if event.type == MOUSEBUTTONDOWN:
                #     self.__init__(self.data,self.pathCopy)
            self._drawMap(ticks)
            pygame.display.update()
            # ticks = self.FPSCLOCK.tick(FPS)
            ticks = self.FPSCLOCK.tick_busy_loop(FPS)

def readAndConvert(filePath):
    rs = []
    with open(filePath) as f:
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
    data = FetchData("Problems/problem_A4.json")
    rsMatrix = readAndConvert("Problems/log.txt")
    rsMatrix = mapPathToAgent(rsMatrix,data)
    pprint(rsMatrix)
    map = Map(data,rsMatrix)
    map.runGame()

if __name__ == "__main__":
    main()
