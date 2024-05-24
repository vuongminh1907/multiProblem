from population import Population
import random

class NSGA2Utils:
    def __init__(self, problem, num_of_individuals=100, num_of_tour_particips=2, tournament_prob=0.9, crossover_param=2, mutation_rate=0.1):
        self.problem = problem
        self.num_of_individuals = num_of_individuals
        self.num_of_tour_particips = num_of_tour_particips
        self.tournament_prob = tournament_prob
        self.crossover_param = crossover_param
        self.mutate_rate = mutation_rate
        
    def create_initial_population(self):
        population = Population()
        for _ in range(self.num_of_individuals):
            individual = self.problem.generate_individual()
            self.problem.calculate_objectives(individual)
            population.append(individual)
        return population
    
    def fast_nondominated_sort(self, population):
        population.fronts = [[]]
        for individual in population:
            individual.domination_count = 0
            individual.dominated_solutions = []
            for other_individual in population:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.append(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1
            if individual.domination_count == 0:
                individual.rank = 0
                population.fronts[0].append(individual)
        i = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i + 1
                        temp.append(other_individual)
            i = i + 1
            population.fronts.append(temp)

    def calculate_crowding_distance(self, front):
        if len(front) > 0:
            solutions_num = len(front)
            for individual in front:
                individual.crowding_distance = 0
            for m in range(len(front[0].objectives)):
                front.sort(key=lambda individual: individual.objectives[m])
                front[0].crowding_distance = 10 ** 9
                front[solutions_num - 1].crowding_distance = 10 ** 9
                m_values = [individual.objectives[m] for individual in front]
                for i in range(1, solutions_num - 1):
                    if (m_values[solutions_num - 1] - m_values[0]) == 0:
                        front[i].crowding_distance += 0
                    else:
                        front[i].crowding_distance += (m_values[i + 1] - m_values[i - 1]) / (m_values[solutions_num - 1] - m_values[0])
    
    def crossover(self, individual1, individual2):
        child1 = self.problem.generate_individual()
        child2 = self.problem.generate_individual()

        sensor1 = individual1.features[0]
        sensor2 = individual2.features[0]

        radius1 = individual1.features[1]
        radius2 = individual2.features[1]
        num_of_sensor = len(sensor1)

        #crossover sensor1 and sensor2 which are permutation of num_of_sensor
        index1 = random.randint(0, num_of_sensor - 1)
        index2 = random.randint(0, num_of_sensor - 1)
        if index1 > index2:
            index1, index2 = index2, index1
        #cross over with new sensors are also permutation of num_of_sensor
        new_gen1 = []
        new_gen2 = []
        for i in range(num_of_sensor):
            if sensor2[i]  not in sensor1[:index1] + sensor1[index2:]:
                new_gen1.append(sensor2[i])
            if sensor1[i] not in sensor2[:index1] + sensor2[index2:]:
                new_gen2.append(sensor1[i])
        child1.features[0] = sensor1[:index1] + new_gen1 + sensor1[index2:]
        child2.features[0] = sensor2[:index1] + new_gen2 + sensor2[index2:]

        #compute new radius
        new_radius1 = []
        new_radius2 = []
        #crossover radius1 and radius2 by averaging radius of each sensor
        for i in range(num_of_sensor):
            index_sensor1 = child1.features[0][i]
            index_sensor2 = child2.features[0][i]
            
            idx1 = sensor1.index(index_sensor1)
            idx2 = sensor2.index(index_sensor1)
            new_radius1.append((radius1[idx1] + radius2[idx2]) / 2)

            idx1 = sensor1.index(index_sensor2)
            idx2 = sensor2.index(index_sensor2)
            new_radius2.append((radius1[idx1] + radius2[idx2]) / 2)
        child1.features[1] = new_radius1
        child2.features[1] = new_radius2
        return child1, child2
    def mutate(self, individual):
        sensor = individual.features[0]
        radius = individual.features[1]
        num_of_sensor = len(sensor)
        #mutate sensor
        if random.random() < self.mutate_rate:
            index1 = random.randint(0, num_of_sensor - 1)
            index2 = random.randint(0, num_of_sensor - 1)
            sensor[index1], sensor[index2] = sensor[index2], sensor[index1]
        #mutate radius
        for i in range(num_of_sensor):
            if random.random() < self.mutate_rate:
                radius[i] = radius[i] + random.uniform(-0.1, 0.1)
                radius[i] = max(0, radius[i])\
    
    def crowding_operator(self, individual1, individual2):
        if individual1.rank < individual2.rank:
            return 1
        elif individual1.rank == individual2.rank and individual1.crowding_distance > individual2.crowding_distance:
            return 1
        else:
            return -1
    
    def __choose_with_prob(self, prob):
        if random.random() <= prob:
            return True
        return False
    
    def tournament(self, population):
        participants = random.sample(population.population, self.num_of_tour_particips)
        best = None
        for participant in participants:
            if best is None or (
                    self.crowding_operator(participant, best) == 1 and self.__choose_with_prob(self.tournament_prob)):
                best = participant
        return best
    
    def create_children(self, population):
        children = []
        while len(children) < self.num_of_individuals:
            parent1 = self.tournament(population)
            parent2 = parent1
            while parent1 == parent2:
                parent2 = self.tournament(population)
            child1, child2 = self.crossover(parent1, parent2)
            self.mutate(child1)
            self.mutate(child2)
            self.problem.calculate_objectives(child1)
            self.problem.calculate_objectives(child2)
            children.append(child1)
            children.append(child2)
        return children


            


        
        


