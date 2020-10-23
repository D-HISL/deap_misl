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

toolbox.register("evaluate", evalOneMax)
#toolbox.register("mate", misl_tools.cxTwoPoint2d)
toolbox.register("mate", misl_tools.cx2d, area_max=50, rounding=round)
toolbox.register("mutate1d", tools.mutFlipBit, indpb=0.05)
toolbox.register("mutate", misl_tools.mutate2d, toolbox=toolbox)
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
