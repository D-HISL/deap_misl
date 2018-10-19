# -*- coding: utf-8 -*-

import array
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def calc(individual, check):
    diff = 0
    for i in range(len(individual)):
        if individual[i] != check[i]:
            diff += 1
    return diff

ZERO_COUNT = 10

CHECK1 = [0] * 0 + [1] * 100
CHECK2 = [0] * ZERO_COUNT + [1] * (100 - ZERO_COUNT)

# 対象問題
def evalMoOneMax(individual):
    l = len(individual)
    return l - calc(individual, CHECK1), l - calc(individual, CHECK2)

toolbox.register("evaluate", evalMoOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selNSGA2)
toolbox.register("migrate", tools.migRing, k=5, selection=tools.selBest, replacement=random.sample)

def main(seed=None):
    # ベースはOneMax DGA
    random.seed(64)

    """
    # 島数
    NBR_DEMES = 3
    # 各島の個体数
    MU = 100
    # 世代
    NGEN = 40
    # 交叉率
    CXPB = 0.5
    # 突然変異率
    MUTPB = 0.2
    # 移住間隔
    MIG_RATE = 5
    """
    # 島数
    NBR_DEMES = 1
    # 各島の個体数
    MU = 100
    # 世代
    NGEN = 100
    # 交叉率
    CXPB = 0.5
    # 突然変異率
    MUTPB = 0.2
    # 移住間隔
    MIG_RATE = 5
    
    demes = [toolbox.population(n=MU) for _ in range(NBR_DEMES)]
    hof = tools.HallOfFame(1)
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    
    logbook = tools.Logbook()
    logbook.header = "gen", "deme", "evals", "std", "min", "avg", "max"
    
    for idx, deme in enumerate(demes):
        for ind in deme:
            ind.fitness.values = toolbox.evaluate(ind)
        logbook.record(gen=0, deme=idx, evals=len(deme), **stats.compile(deme))
        hof.update(deme)
    print(logbook.stream)
    
    gen = 1
    while gen <= NGEN:
        for idx, deme in enumerate(demes):
            # OneMax DGAのアルゴリズム。これだと結果が良くない
            """
            deme[:] = toolbox.select(deme, len(deme))
            deme[:] = algorithms.varAnd(deme, toolbox, cxpb=CXPB, mutpb=MUTPB)
            
            invalid_ind = [ind for ind in deme if not ind.fitness.valid]
            for ind in invalid_ind:
                ind.fitness.values = toolbox.evaluate(ind)
            """

            offspring = algorithms.varOr(deme, toolbox, MU*2, CXPB, MUTPB)
            #offspring = algorithms.varOr(deme, toolbox, MU, CXPB, MUTPB)
            
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            for ind in invalid_ind:
                ind.fitness.values = toolbox.evaluate(ind)

            deme[:] = toolbox.select(deme + offspring, MU)
            
            logbook.record(gen=gen, deme=idx, evals=len(deme), **stats.compile(deme))
            hof.update(deme)
        print(logbook.stream)
            
        if gen % MIG_RATE == 0:
            toolbox.migrate(demes)
        gen += 1
    
    return demes, logbook, hof
        
if __name__ == "__main__":
    demes, logbook, hof = main()
    # 配列の配列をフラット化
    from itertools import chain
    pop = list(chain.from_iterable(demes))
    pop.sort(key=lambda x: x.fitness.values)

    import matplotlib.pyplot as plt
    # 
    front = numpy.array([ind.fitness.values for ind in pop])
    plt.scatter(front[:,0], front[:,1], c="b")
    plt.axis("tight")
    plt.show()
