from ReadJson import FetchData
from shapely.geometry import Point
from plots import plot_map
import matplotlib.pylab as plt
from behold import Behold
from pprint import pprint

class GridCell(object):
    def __init__(self,pos):
        self.pos = pos
        self.neighbors = []

class Node(object):
    def __init__(self,pos):
        self.pos = pos
        self.neighbors = []

def isInFreeSpace(point,map):
    point = Point(point)
    if not map.boundary_polygon_polygon.contains(point):
        return False
    else:
        for poly in map.obstacles_polygon:
            if poly.contains(point):
                return False
    return True

def gridizeMapWithDic(map):
    graph = {}
    boundary = map.boundary_polygon_list
    cellSize = map.sensor_range*1.4
    directions = [(cellSize / 2., 0), (-cellSize / 2., 0), (0, cellSize / 2.), (0, -cellSize / 2.)]
    cornorDirections = [(cellSize / 2., cellSize / 2.), (-cellSize / 2., -cellSize / 2.),
                        (-cellSize / 2., cellSize / 2.), (cellSize / 2., -cellSize / 2.)]
    for cornerDir in cornorDirections:
        cornerPos = (boundary[0][0] + cornerDir[0], boundary[0][1] + cornerDir[1])
        if isInFreeSpace(cornerPos,map):
            finalCornorPos = cornerPos
            break
    graph[finalCornorPos] = []
    q = [finalCornorPos]
    # visited = set()
    qHistory = set(finalCornorPos)
    while q:
        cell = q.pop()
        # visited.add(cell.pos)
        for dirc in directions:
            newPos = (cell[0] + dirc[0], cell[1] + dirc[1])
            if isInFreeSpace(newPos, map):
                graph[newPos] = [cell]
                if newPos not in graph[cell]:
                    graph[cell].append(newPos)
                # if newCell.pos not in visited :
                #     print(newCell.pos)
                #     cell.neighbors.append(newCell)
                if newPos not in qHistory:
                    q.append(newPos)
                    qHistory.add(newPos)
    return graph,cellSize

def gridizeMap(map):
    boundary = map.boundary_polygon_list
    #cellSize is 2 times the square ascribed to the sensor circle?????
    cellSize = map.sensor_range*1.4
    # cellSize =1
    directions = [(cellSize/2.,0),(-cellSize/2.,0),(0,cellSize/2.),(0,-cellSize/2.)]
    # directions = [(cellSize / 2, 0), (0, cellSize / 2)]
    # directions = [(cellSize / 2., 0),(0, -cellSize / 2.)]
    cornorDirections = [(cellSize/2.,cellSize/2.),(-cellSize/2.,-cellSize/2.),(-cellSize/2.,cellSize/2.),(cellSize/2.,-cellSize/2.)]
    for cornerDir in cornorDirections:
        cornerPos = (boundary[0][0]+cornerDir[0],boundary[0][1]+cornerDir[1])
        flag =isInFreeSpace(cornerPos,map)
        if flag:
            finalCornorPos = cornerPos
            break
    cornorCell = GridCell(finalCornorPos)
    q = [cornorCell]
    # visited = set()
    qHistory = set(cornorCell.pos)
    while q:
        cell = q.pop(0)
        # visited.add(cell.pos)
        for dirc in directions:
            newPos = (cell.pos[0]+dirc[0],cell.pos[1]+dirc[1])
            if isInFreeSpace(newPos,map):
                newCell = GridCell(newPos)
                cell.neighbors.append(newCell)
                # if newCell.pos not in visited :
                #     print(newCell.pos)
                #     cell.neighbors.append(newCell)
                if newCell.pos not in qHistory:
                    q.append(newCell)
                    qHistory.add(newCell.pos)
    return cornorCell,cellSize

def showGrid(grid):
    q = [grid]
    qHistory = set(grid.pos)
    while q:
        cell = q.pop(0)
        for neighbor in cell.neighbors:
            if neighbor.pos not in qHistory:
                q.append(neighbor)
                qHistory.add(neighbor.pos)
                plt.plot(neighbor.pos[0],neighbor.pos[1],'bo')

def showDicGrid(grid):
    for cell in grid:
        plt.plot(cell[0],cell[1],"bo")

def possibleNextCell(agentPossition):
    pass

def buildingSpanningTree(grid,cellSize,map):
    numOfSubtree = len(map.start_positions)
    pass

def MSTC(spanningTree):
    pass

def main():
    data = FetchData("Problems/problem_A12.json")

    grid,cellSize = gridizeMapWithDic(data)
    pprint (grid)
    showDicGrid(grid)
    plot_map(data)
    plt.show()


    # grid = gridizeMap(data)
    # showGrid(grid)
    # plot_map(data)
    # plt.show()

if __name__ == "__main__":
    main()
