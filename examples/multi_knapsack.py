# -*- coding: utf-8 -*-

import random
import operator

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from deap_misl import tools as misl_tools

NUM_ITEMS = 100

w = [
    [94, 74, 77, 74, 29, 11, 73, 80, 81, 82, 75, 42, 44, 57, 20, 20, 99, 95, 52, 81, 68, 16, 79, 30, 16, 90, 21, 49, 70, 78, 77, 21, 84, 19, 65, 38, 25, 43, 99, 75, 80, 10, 44, 26, 21, 74, 20, 22, 81, 89, 15, 35, 24, 16, 43, 75, 25, 76, 48, 75, 15, 23, 10, 81, 81, 67, 58, 77, 49, 16, 65, 74, 14, 41, 74, 74, 17, 12, 95, 29, 75, 61, 59, 37, 75, 90, 17, 79, 15, 88, 76, 93, 98, 80, 33, 39, 96, 71, 39, 49],
    [55, 10, 97, 73, 69, 23, 62, 47, 90, 62, 96, 88, 95, 61, 94, 16, 91, 61, 27, 18, 96, 77, 14, 36, 17, 56, 83, 41, 52, 69, 97, 45, 94, 45, 47, 28, 82, 13, 82, 39, 28, 41, 55, 12, 50, 32, 97, 87, 36, 11, 20, 37, 87, 91, 19, 22, 89, 54, 20, 78, 52, 35, 18, 96, 54, 10, 39, 17, 51, 40, 25, 84, 54, 31, 97, 37, 63, 39, 60, 87, 63, 37, 13, 31, 84, 90, 84, 57, 21, 64, 63, 21, 95, 83, 81, 45, 68, 89, 100, 14]
]
p = [
    [57, 94, 59, 83, 82, 91, 42, 84, 85, 18, 94, 18, 31, 27, 31, 42, 58, 57, 55, 97, 79, 10, 34, 100, 98, 45, 19, 77, 56, 25, 60, 22, 84, 89, 12, 46, 20, 85, 42, 94, 20, 65, 27, 34, 27, 91, 17, 56, 23, 89, 18, 11, 91, 79, 14, 99, 45, 73, 81, 96, 51, 96, 63, 40, 93, 87, 71, 54, 74, 15, 32, 57, 70, 62, 12, 71, 57, 97, 48, 33, 42, 15, 39, 91, 17, 63, 81, 49, 60, 90, 87, 25, 15, 30, 76, 76, 53, 59, 40, 59],
    [20, 19, 20, 66, 48, 100, 13, 87, 62, 73, 53, 79, 17, 93, 78, 22, 85, 86, 56, 56, 44, 86, 94, 93, 57, 31, 20, 35, 70, 79, 58, 24, 84, 12, 17, 43, 35, 47, 92, 38, 93, 50, 27, 100, 36, 30, 23, 22, 56, 73, 55, 32, 75, 42, 82, 80, 55, 48, 93, 28, 26, 42, 96, 93, 16, 39, 46, 80, 24, 87, 37, 73, 81, 38, 98, 13, 91, 85, 17, 59, 58, 56, 93, 66, 64, 17, 10, 33, 28, 97, 25, 42, 17, 23, 37, 46, 52, 33, 26, 90]
]
c = [2732, 2753]

creator.create("Fitness", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, NUM_ITEMS)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalKnapsack(individual):
    f = [0, 0]
    for i in range(2):
        if sum(map(operator.mul, w[i], individual)) <= c[i]:
            f[i] = sum(map(operator.mul, p[i], individual))
    return f

toolbox.register("evaluate", evalKnapsack)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", misl_tools.selNSGA2)
#SPEA2はまだできていない
#toolbox.register("select", misl_tools.selSPEA2)

# examples/ga/msga2.pyベース
# examplesではZDT1解いているのでパラメータが最適でない可能性あり
def main():
    random.seed(64)

    # 個体数
    #MU = 100
    MU = 300
    # 世代
    #NGEN = 250
    NGEN = 1000
    # 交叉率
    CXPB = 0.9
    # 突然変異率
    #MUTPB = 0.2
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    
    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"
    
    pop = toolbox.population(n=MU)
    
    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)

    # 初期状態の距離計算
    pop = toolbox.select(pop, len(pop))

    logbook.record(gen=0, evals=len(pop), **stats.compile(pop))
    print(logbook.stream)
    
    gen = 1
    while gen <= NGEN:
        #chosen_by_variable = False
        #chosen_by_variable = True
        chosen_by_variable = (gen % 2 == 0)

        offspring = misl_tools.selTournamentDCD(pop, len(pop), chosen_by_variable)
        offspring = [toolbox.clone(ind) for ind in offspring]

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)
            
            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        for ind in invalid_ind:
            ind.fitness.values = toolbox.evaluate(ind)

        pop = toolbox.select(pop + offspring, MU, chosen_by_variable)
            
        logbook.record(gen=gen, evals=len(invalid_ind), **stats.compile(pop))
        print(logbook.stream)
        
        gen += 1
    
    return pop, logbook

if __name__ == "__main__":
    pop, logbook = main()
    pop.sort(key=lambda x: x.fitness.values)

    import matplotlib.pyplot as plt

    front = numpy.array([ind.fitness.values for ind in pop])
    plt.scatter(front[:,0], front[:,1], c="b")
    plt.axis("tight")
    plt.show()
