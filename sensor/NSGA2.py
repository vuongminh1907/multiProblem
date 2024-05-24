
import math
import matplotlib.pyplot as plt
import random

from problem import Problem
from utils import NSGA2Utils
from evolution import Evolution

def compute_distance(sensor, target):
    return math.sqrt((sensor[0] - target[0])**2 + (sensor[1] - target[1])**2)

# compute num disjoint set of targets
def f1(x,sensor_positions,target_positions):
    max_value = 1000000
    sensor = x[0]
    #convert sensor to integer
    sensor = [int(i) for i in sensor]
    radius = x[1]
    num_sensor = len(sensor)
    num_target = len(target_positions)
    num_disjoint_set = 0
    detected_target = set()
    for i in range(num_sensor):
        set_target_detected = set()
        for j in range(num_target):
            if compute_distance(sensor_positions[sensor[i]], target_positions[j]) <= radius[i]:
                set_target_detected.add(j)
        detected_target = detected_target.union(set_target_detected)
        if len(detected_target) == num_target:
            num_disjoint_set = num_disjoint_set + 1
            detected_target = set()
    return max_value - (num_disjoint_set*num_target + len(detected_target))

def f2(x, energy_rate=0.1):
    sensor = x[0]
    radius = x[1]
    num_sensor = len(sensor)
    energy = 0
    for i in range(num_sensor):
        energy += energy_rate*radius[i]**2
    return energy


num_sensor = 50
num_target = 5

range_of_observation = [0, 10]
sensor_positions = [[random.uniform(range_of_observation[0], range_of_observation[1]) for _ in range(2)] for _ in range(num_sensor)]
target_positions = [[random.uniform(range_of_observation[0], range_of_observation[1]) for _ in range(2)] for _ in range(num_target)]

#plot the sensor and target positions
plt.figure()
for i in sensor_positions:
    plt.scatter(i[0], i[1], c='r', marker='o')
for i in target_positions:
    plt.scatter(i[0], i[1], c='b', marker='x')
plt.xlabel('x', fontsize=15)
plt.ylabel('y', fontsize=15)
plt.title('Sensor and Target positions')
plt.show()
problem = Problem(objectives=[f1, f2], num_sensor=num_sensor, sensor_range=[0, 1], radius_range=[0, 10], sensor_positions=sensor_positions, target_positions=target_positions)
evo = Evolution(problem,num_of_generations=100)
front = evo.evolve()


#plot the pareto front for the all evo.evolve() in one plot
plt.figure()
for gen_idx, i in enumerate(front):
    func = [i.objectives for i in i]
    plt.scatter([1000000-i[0] for i in func],[i[1] for i in func],label = 'Pareto '+str(gen_idx))
plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
plt.title('Pareto front after the optimization')
plt.legend(title='Parento Fronts')
plt.show()

#plot the pareto front for the last evo.evolve() in one plot
plt.figure()
func = [i.objectives for i in front[0]]
plt.scatter([1000000-i[0] for i in func],[i[1] for i in func])
plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
plt.title('Pareto front after the optimization')
plt.show()



