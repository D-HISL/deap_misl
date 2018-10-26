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
toolbox.register("select", misl_tools.selNSGA3)
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

    front = numpy.array([ind.fitness.values for ind in pop if ind.fitness.values[0] > 2000 and ind.fitness.values[1] > 2000])
    plt.scatter(front[:,0], front[:,1], c="b")

    optimal = [
        [3235, 4037], [3246, 4031], [3271, 4029], [3340, 4028], [3350, 4024], 
        [3364, 4021], [3415, 4017], [3431, 4009], [3453, 4003], [3466, 4001], 
        [3469, 4000], [3481, 3998], [3485, 3993], [3490, 3990], [3497, 3989], 
        [3511, 3987], [3512, 3986], [3540, 3982], [3556, 3975], [3568, 3971], 
        [3582, 3970], [3595, 3966], [3616, 3956], [3632, 3949], [3635, 3938], 
        [3645, 3937], [3653, 3936], [3660, 3935], [3666, 3926], [3672, 3925], 
        [3688, 3919], [3690, 3914], [3704, 3912], [3732, 3908], [3749, 3893], 
        [3751, 3891], [3753, 3885], [3762, 3881], [3763, 3878], [3778, 3875], 
        [3779, 3871], [3787, 3870], [3791, 3863], [3797, 3862], [3806, 3860], 
        [3822, 3857], [3825, 3851], [3831, 3848], [3832, 3845], [3833, 3843], 
        [3834, 3842], [3838, 3839], [3839, 3836], [3855, 3832], [3860, 3830], 
        [3870, 3826], [3879, 3817], [3884, 3813], [3888, 3812], [3907, 3806], 
        [3909, 3801], [3918, 3792], [3924, 3786], [3927, 3783], [3929, 3778], 
        [3938, 3773], [3952, 3769], [3963, 3761], [3964, 3748], [3969, 3747], 
        [3970, 3739], [3977, 3738], [3990, 3731], [3994, 3724], [3996, 3722], 
        [3997, 3718], [4009, 3717], [4010, 3716], [4014, 3705], [4019, 3700], 
        [4041, 3697], [4050, 3680], [4056, 3666], [4064, 3660], [4071, 3649], 
        [4074, 3646], [4082, 3640], [4089, 3635], [4094, 3612], [4098, 3605], 
        [4100, 3603], [4102, 3602], [4121, 3595], [4122, 3569], [4125, 3566], 
        [4128, 3560], [4130, 3555], [4136, 3554], [4139, 3546], [4142, 3537], 
        [4151, 3534], [4152, 3528], [4164, 3521], [4168, 3505], [4174, 3499], 
        [4175, 3491], [4182, 3478], [4185, 3466], [4197, 3462], [4199, 3443], 
        [4205, 3437], [4215, 3423], [4218, 3400], [4220, 3368], [4230, 3367], 
        [4236, 3338], [4246, 3319], [4248, 3300], [4250, 3278], [4262, 3274], 
        [4266, 3215]
    ]
    optimal = numpy.array(optimal)
    plt.scatter(optimal[:,0], optimal[:,1], c="r")

    plt.axis("tight")
    plt.show()
