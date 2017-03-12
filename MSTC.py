from ReadJson import FetchData
from shapely.geometry import Point
from plots import plot_map
import matplotlib.pylab as plt

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


def gridizeMap(map):
    boundary = map.boundary_polygon_polygon
    #cellSize is 2 times the square ascribed to the sensor circle?????
    cellSize = map.sensor_range*1.4
    # directions = [(cellSize/2,0),(-cellSize/2,0),(0,cellSize/2),(0,-cellSize/2)]
    directions = [(cellSize / 2, 0), (0, cellSize / 2)]
    cornorDirections = [(cellSize/2,cellSize/2),(-cellSize/2,-cellSize/2),(-cellSize/2,cellSize/2),(cellSize/2,-cellSize/2)]
    for cornerDir in cornorDirections:
        print(cornerDir)
        cornerPos = (map.boundary_polygon_list[0][0]+cornerDir[0],map.boundary_polygon_list[0][1]+cornerDir[1])
        if isInFreeSpace(cornerPos,map):
            finalCornorPos = cornerPos
            break
    cornorCell = GridCell(finalCornorPos)
    q = [cornorCell]
    visited = set()
    while q:
        cell = q.pop()
        visited.add(cell.pos)
        for dir in directions:
            newPos = (cell.pos[0]+dir[0],cell.pos[1]+dir[1])
            if not isInFreeSpace(newPos,map):
                continue
            else:
                newCell = GridCell(newPos)
                # newCell.neighbors.append(cell)
                cell.neighbors.append(newCell)
                if newCell.pos not in visited:
                    # print("here")
                    q.append(newCell)
    return cornorCell

def showGrid(grid):
    print("here")
    q = [grid]
    visited = set()
    while q:
        cell = q.pop()
        visited.add(cell)
        print(cell.pos,len(cell.neighbors))
        for neighbor in cell.neighbors:
            print(neighbor.pos)
            q.append(neighbor)
            plt.plot(neighbor.pos,'bo')



def buildingSpanningTree(grid):
    pass

def MSTC(spanningTree):
    pass

def main():
    data = FetchData("Problems/problem_A12.json")
    grid = gridizeMap(data)
    showGrid(grid)
    plot_map(data)
    plt.show()
    pass

if __name__ == "__main__":
    main()
