from individual import Individual
import random


class Problem:

    def __init__(self, objectives, num_sensor, sensor_range=None, radius_range=None,sensor_positions=None, target_positions=None):
        self.num_of_objectives = len(objectives)
        self.num_sensor = num_sensor
        self.objectives = objectives
        self.sensor_range = sensor_range
        self.radius_range = radius_range
        self.sensor_positions = sensor_positions
        self.target_positions = target_positions

    def generate_individual(self):
        individual = Individual()
        #create sensor is permutation of num_sensor
        sensor = random.sample(range(self.num_sensor), self.num_sensor)
        #create radius
        radius = [round(random.uniform(self.radius_range[0], self.radius_range[1]), 1) for _ in range(self.num_sensor)]
        individual.features = [sensor, radius]
        return individual

    def calculate_objectives(self, individual):
        f1 = self.objectives[0]
        f2 = self.objectives[1]
        individual.objectives = [f1(individual.features, self.sensor_positions, self.target_positions), f2(individual.features)]