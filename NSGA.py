from nsga2.problem import Problem
from nsga2.evolution import Evolution
import matplotlib.pyplot as plt
import math


def f1(x):
    s = 0
    for i in range(len(x) - 1):
        s += -10 * math.exp(-0.2 * math.sqrt(x[i] ** 2 + x[i + 1] ** 2))
    return s


def f2(x):
    s = 0
    for i in range(len(x)):
        s += abs(x[i]) ** 0.8 + 5 * math.sin(x[i] ** 3)
    return s


problem = Problem(num_of_variables=2, objectives=[f1, f2], variables_range=[(-5, 5)], same_range=True, expand=False)
evo = Evolution(problem, mutation_param=20,num_of_generations=100)


#plot the pareto front for the all evo.evolve() in one plot
plt.figure()
for gen_idx, i in enumerate(evo.evolve()):
    func = [i.objectives for i in i]
    plt.scatter([i[0] for i in func],[i[1] for i in func],label = 'Pareto '+str(gen_idx))
plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
plt.title('Pareto front after the optimization')
plt.legend(title='Parento Fronts')
plt.show()


'''
func = [i.objectives for i in evo.evolve()[0]]

function1 = [i[0] for i in func]
function2 = [i[1] for i in func]
plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
plt.scatter(function1, function2)
plt.show()
'''