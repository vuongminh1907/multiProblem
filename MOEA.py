import random 
import matplotlib.pyplot as plt 
import math

def function1(x):
    s = 0
    for i in range(len(x) - 1):
        s += -10 * math.exp(-0.2 * math.sqrt(x[i] ** 2 + x[i + 1] ** 2))
    return s

def function2(x):
    s = 0
    for i in range(len(x)):
        s += abs(x[i]) ** 0.8 + 5 * math.sin(x[i] ** 3)
    return s

def main_func(x,weight):
    return weight[0]*function1(x) + weight[1]*function2(x)

def min_index_value(population,weight):
    min_value = main_func(population[0],weight)
    min_index = 0
    for i in range(1,len(population)):
        if main_func(population[i],weight) < min_value:
            min_value = main_func(population[i],weight)
            min_index = i
    return min_index,min_value
def max_index_value(population,weight):
    max_value = main_func(population[0],weight)
    max_index = 0
    for i in range(1,len(population)):
        if main_func(population[i],weight) > max_value:
            max_value = main_func(population[i],weight)
            max_index = i
    return max_index,max_value

#write function non_dominated_sort to sort the population based on the non-dominated sort with no weights
def non_dominated_sort(population):
    front = [[]]
    S = [[] for _ in range(len(population))]
    n = [0 for _ in range(len(population))]
    rank = [0 for _ in range(len(population))]
    for p in range(len(population)):
        S[p] = []
        n[p] = 0
        for q in range(len(population)):
            if function1(population[p]) < function1(population[q]) and function2(population[p]) < function2(population[q]):
                if q not in S[p]:
                    S[p].append(q)
            elif function1(population[p]) > function1(population[q]) and function2(population[p]) > function2(population[q]):
                n[p] += 1
        if n[p] == 0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)
    i = 0
    while front[i] != []:
        Q = []
        for p in front[i]:
            for q in S[p]:
                n[q] -= 1
                if n[q] == 0:
                    rank[q] = i + 1
                    if q not in Q:
                        Q.append(q)
        i += 1
        front.append(Q)
    return front[:-1]



def MOEA():
    # Parameters
    N = 100 # Population size
    T = 1000 # Number of iterations
    n = 3   # Number of variables
    
    weights = [[0.5,0.5],[0.4,0.6],[0.6,0.4]]
    # Initialization
    population_init = [[random.uniform(-5,5) for _ in range(n)] for _ in range(N)]
    weight = weights[0]
    log_result = [[] for _ in range(len(weights))]

    #plot the pareto front
    plt.figure()
    x = [function1(i) for i in population_init]
    y = [function2(i) for i in population_init]
    plt.scatter(x,y)
    plt.xlabel('Function 1')
    plt.ylabel('Function 2')
    plt.title('Pareto front before the optimization')
    plt.show()

    # best individual for each weight
    best_individual = [[0 for _ in range(n)] for _ in range(len(weights))]
    # Main loop

    for i, weight in enumerate(weights):
        log_result[i] = []
        population = population_init

        for t in range(T):
                # Select a random weight
                # weight = random.choice(weights)
                # Select a random individual
                individual1 = random.choice(population)
                individual2 = random.choice(population)
                individual = [(individual1[i] + individual2[i]) / 2.0 for i in range(n)]
                # Mutate the individual
                mutation = [individual[j] + random.uniform(-0.2,0.2) for j in range(n)]
                # Calculate the fitness
                fitness = main_func(individual,weight)
                mutation_fitness = main_func(mutation,weight)
                # Update the population
                if mutation_fitness < fitness:
                    individual = mutation
                # Replace the worst individual
                index,value = max_index_value(population,weight)
                if main_func(individual,weight) < value:
                    population[index] = individual
                # Log the result
                log_result[i].append(min_index_value(population,weight)[1])
        # Update the best individual
        if min_index_value(population,weight)[1] < main_func(best_individual[i],weight):
            best_individual[i] = population[min_index_value(population,weight)[0]]
        
        
        front = non_dominated_sort(population)
        
        #plot the pareto front for front in one plot
        plt.figure()
        for gen_idx, i in enumerate(front):
            func = [population[i] for i in i]
            plt.scatter([function1(i) for i in func],[function2(i) for i in func],label = 'Pareto '+str(gen_idx))
        plt.xlabel('Function 1', fontsize=15)
        plt.ylabel('Function 2', fontsize=15)
        plt.title('Pareto front after the optimization weight' + str(weight))
        plt.legend(title='Parento Fronts')
        plt.show()


        '''
        #plot the pareto after the optimization
        plt.figure()
        x = [function1(i) for i in population]
        y = [function2(i) for i in population]
        plt.scatter(x,y)
        plt.xlabel('Function 1')
        plt.ylabel('Function 2')
        plt.title('Pareto front after the optimization weight' + str(weight))
        plt.show()
        '''
        
                
    #plot the results with different weights
    plt.figure()
    for i in range(len(weights)):
        plt.plot(log_result[i])
    plt.xlabel('Iteration')
    plt.ylabel('Function value')
    plt.title('Results with different weights')
    plt.show()

    print('Best individual for each weight:',best_individual)  


if __name__ == '__main__':
    MOEA()
    
