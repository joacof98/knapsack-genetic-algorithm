from genetic_solution import *
from functools import partial
from collections import namedtuple
import time
'''
This is an example of solution for the knapsack problem
using the genetic algorithm.
'''
Thing = namedtuple('Thing', ['name', 'value', 'weight'])

things_example = [
    Thing('Laptop', 500, 2200),
    Thing('Headphones', 150, 160),
    Thing('Coffee Mug', 60, 350),
    Thing('Notepad', 40, 333),
    Thing('Water Bottle', 30, 192),
]

# Constants
POPULATION_NUMBER = 10
GENOME_LENGTH = len(things_example)

# For evaluating the aptitude of one individual
# This function is defined here because is specific to this problem.
def fitness(genome, things, weight_limit: int):
    if len(genome) != len(things):
        raise ValueError("genome and things must be of same length")

    weight = 0
    value = 0
    for i, thing in enumerate(things):
        if genome[i] == 1:
            weight += thing.weight
            value += thing.value

            if weight > weight_limit:
                return 0

    return value

def from_genome(genome, things):
    result = []
    for i, thing in enumerate(things):
        if genome[i] == 1:
            result += [thing]

    return result

start = time.time()
population, generation = run_evolution(
    populate_func = partial(generate_population, POPULATION_NUMBER, GENOME_LENGTH),
    fitness_func = partial(fitness, things=things_example, weight_limit = 3000),
    fitness_limit = 740,
    selection_func = selection_pair,
    crossover_func = single_point_crossover,
    mutation_func = mutation,
    generation_limit = 100
)
end = time.time()

print(f"Number of generations: {generation}")
print(f"Best solution: {from_genome(population[0], things_example)}")
print(f'Time: {end - start}')

# Aclaration:
# I know before hand that '740' is the best value for this set of things.