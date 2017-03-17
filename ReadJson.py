import json
from pprint import pprint
import numpy as np
from shapely.geometry import  Polygon

class FetchData(object):
    def __init__(self,fileName):
        self.data = self.readJson(fileName)
        self.getValues()


    def readJson(self,fileName):
        with open(fileName) as data_file:
            data = json.load(data_file)
        return data

    def showData(self):
        pprint(self.data)

    def getValues(self):
        self.L_car = self.data['L_car']
        self.a_max = self.data['a_max']
        self.sensor_range = self.data["sensor_range"]
        self.boundary_polygon_list = self.data['boundary_polygon']
        self.boundary_polygon_polygon = Polygon(self.boundary_polygon_list)
        self.goal_positions = self.getGoalPositions()
        self.goal_vel = self.data['goal_vel']
        self.items = self.getItems()
        self.k_friction = self.data['k_friction']
        self.omega_max = self.data['omega_max']
        self.phi_max = self.data['phi_max']
        self.start_positions = self.getStartPositions()
        self.start_vel = self.data['start_vel']
        self.v_max = self.data['v_max']
        self.obstacles_list = self.getObstacles()
        self.obstacles_polygon = self.buildPolygonObstacles()
        self.approximatedBoundary = self.getApproximatedBoundary()
        self.allListPolygons = [self.boundary_polygon_list] + self.obstacles_list

    def getObstacles(self):
        obstacles = []
        for key in self.data.keys():
            if key.startswith("polygon"):
                obstacles.append(self.data[key])
        return obstacles

    def getItems(self):
        items = []
        for key in self.data.keys():
            if key.startswith("item"):
                items.append(tuple(self.data[key]))
        return items

    def getStartPositions(self):
        items = []
        for key in self.data.keys():
            if key.startswith("start_pos"):
                items.append(self.data[key])
        return items

    def getGoalPositions(self):
        items = []
        for key in self.data.keys():
            if key.startswith("goal_pos"):
                items.append(self.data[key])
        return items

    def buildPolygonObstacles(self):
        polygons = []
        # build obstacles inside boundary
        for listPolygon in self.obstacles_list:
            polygons.append(Polygon(listPolygon))
        return polygons

    def getApproximatedBoundary(self):
        x = []
        y = []
        for vertex in self.boundary_polygon_list:
            x.append(vertex[0])
            y.append(vertex[1])
        return (min(x), min(y), max(x), max(y))


if __name__ == "__main__":
    data = FetchData("Problems/problem_A12.json")
    data.showData()
    # print(len(data.items))
    # print(data.start_positions)
    # print(data.goal_positions)
    # # data.showData()
    # with open('data.json', 'w') as outfile:
    #     json.dump(data.data, outfile)
    # print(data.boundary_polygon_list)
