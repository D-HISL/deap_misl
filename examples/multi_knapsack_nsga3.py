# -*- coding: utf-8 -*-

import random
import numpy

import argparse

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from deap_misl import tools as misl_tools

import utils

parser = argparse.ArgumentParser()
parser.add_argument("--problem", default='100_2')
args = parser.parse_args()

problems = {
    '100_2': {'items': 100, 'data_func': utils.knapsack.knapsack_100_2},
    '250_2': {'items': 250, 'data_func': utils.knapsack.knapsack_250_2},
    '500_2': {'items': 500, 'data_func': utils.knapsack.knapsack_500_2}
}

NUM_ITEMS = problems[args.problem]['items']
weights, profits, capacities, pareto = problems[args.problem]['data_func']()

creator.create("Fitness", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, NUM_ITEMS)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", utils.knapsack.evaluate, weights=weights, profits=profits, capacities=capacities)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", misl_tools.selNSGA3)

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

        offspring = misl_tools.selTournamentDCD(pop, len(pop))
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

        pop = toolbox.select(pop + offspring, MU)
            
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

    optimal = numpy.array(pareto)
    plt.scatter(optimal[:,0], optimal[:,1], c="r")

    plt.axis("tight")
    plt.show()
