import matplotlib.pylab as plt
from ReadJson import FetchData
from matplotlib.patches import Polygon
import numpy as np
import matplotlib.patches as mpatches
import itertools
from shapely.geometry import LineString

def plot_boundary_polygon(boundary_polygon):
	np_boundary = np.asarray(boundary_polygon)
	poly = Polygon(np_boundary,facecolor='none')
	plt.gca().add_patch(poly)
	xmin = min(np_boundary.T[0])
	xmax = max(np_boundary.T[0])
	ymin = min(np_boundary.T[1])
	ymax = max(np_boundary.T[1])
	plt.xlim((xmin-3,xmax+3))
	plt.ylim((ymin-3,ymax+3))
	plt.gca().set_aspect('equal', adjustable='box')

def plot_items(items):
	for x,y in items:
		plt.plot(x,y,'x')

def plot_cover_range(stations,sensorRange):
	for x,y in stations:
		c = mpatches.Circle((x, y), sensorRange, facecolor="none",
							edgecolor="red", linewidth=1)
		plt.gca().add_patch(c)

def plot_obstacles(obstacles):
	for i in range(len(obstacles)):
		poly = Polygon(np.asarray(obstacles[i]),facecolor='yellow')
		plt.gca().add_patch(poly)

def plot_kinematic_point(location,velocity,symbol):
	plt.plot(location[0],location[1],symbol)
	vx = [location[0],location[0]+velocity[0]]
	vy = [location[1],location[1]+velocity[1]]
	plt.plot(vx,vy,'r')

def plot_start_and_end_point(startPoints,endPoints):
	# plot_kinematic_point(startPoint,startAngel,'r*')
	# plot_kinematic_point(endPoint,endAngel,'rs')
	for x,y in startPoints:
		plt.plot(x,y,'*')
	for x,y in endPoints:
		plt.plot(x,y,'s')

def plot_convex_net(data):
	obstacles = data.obstacles_polygon
	points = data.boundary_polygon_list
	for obs in data.obstacles_list:
		points +=obs
	for point1,point2 in itertools.permutations(points,2):
		line = LineString([point1,point2])
		nocross = True
		for obs in obstacles:
			if line.crosses(obs) or line.within(obs):
				nocross = False
				break
		if nocross:
			plt.plot([point1[0],point2[0]],[point1[1],point2[1]])

def plot_path(path):
	for i in range(len(path)-1):
		plt.plot([path[i][0],path[i+1][0]],[path[i][1],path[i+1][1]])


def plot_map(data):
	#takes FetchData instance
	obstacles = data.obstacles_list
	startPoints = data.start_positions
	endPoints = data.goal_positions
	boundary_polygon = data.boundary_polygon_list
	items = data.items


	plot_boundary_polygon(boundary_polygon=boundary_polygon)
	# plot_convex_net(data)
	plot_obstacles(obstacles)
	plot_start_and_end_point(startPoints,endPoints)
	plot_items(items)


if __name__ == '__main__':
	data = FetchData('Problems/problem_A5_2.json')
	print(data.sensor_range)
	plot_map(data)
	plt.show()
