# MultiAgent_A2

###Task 1: Multi-agent Static Guarding
Given a polygonal environment, a set of points of interest, and a sensor range. Position N guards in a such a way that maximizes the number of points p such that the line of sight between the point and one of the guards is obstacle free and shorter than the sensor range.

###Task 2: Multi-agent Short Range Search
Given a polygonal environment, a set of points of interest, and a sensor range. Move N guards in a such a way that minimizes the time in which all points have been seen by at lest one of the guards.
This problem corresponds to planning paths for lawn mowers, vacuum cleaners, and UAV search over mostly obstacle free terrain.

###Task 3: Multi-agent Long Range Search
Same as above with a sensor range that is long compared to the typical spacing between the points of interest.
This problem corresponds to indoor search of security robots, either UGVs and UAVs.

###Task 4: Multi-agent Point of Interest Search
Same as above with a short sensor range and sparse points of interest compared to the obstacle distances. If the sensor range is 0 this problem corresponds to a multi-TSP.

###Task 5: Formation and obstacle avoidance
Given a polygonal environment and a set of agents with starting positions and goal positions, move the agents to minimize the sum of completion time and formation error in the following form:

```tex
$$ \int^T_01dt + k\int_0^T(||p_i-p_j||-d_{ij})^2dt\ $$
```

where T is the time of reaching the goal positions and d_ij is the desired distance between vehicles i and j. The parameters "goal_pos" in the json-files, define the desired formation, so d_ij can be computed from them. Assume k=1 for this task.

