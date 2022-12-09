import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from deap_misl import tools as misl_tools

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("attr_row", tools.initRepeat, list, toolbox.attr_bool, 10)

# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_row, 10)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    return sum([sum(row) for row in individual]),

def adaptive_area_max(count):
    # 交叉は個体数に対して半分の回数が呼ばれる（2個体ずつ渡されるため）
    # また、交叉率を掛けることで「現在の世代」を推定できる
    gen = int(count / ((300 / 2) * 0.5))
    # 最大面積を50とし、1世代ごとに最大面積を小さくしていく
    return 50 - gen

adaptive_cx2d = misl_tools.AdaptiveParameterWrapper(misl_tools.cx2d, "area_max", adaptive_area_max)

toolbox.register("evaluate", evalOneMax)
#toolbox.register("mate", misl_tools.cxTwoPoint2d)
#toolbox.register("mate", misl_tools.cx2d, area_max=50, rounding=round)
toolbox.register("mate", adaptive_cx2d, rounding=round)
toolbox.register("mutate1d", tools.mutFlipBit, indpb=0.05)
toolbox.register("mutate", misl_tools.mutSimple2dExtend, mut1d=toolbox.mutate1d)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(64)
    
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40, 
                                   stats=stats, halloffame=hof, verbose=True)
    
    return pop, log, hof

if __name__ == "__main__":
    main()
