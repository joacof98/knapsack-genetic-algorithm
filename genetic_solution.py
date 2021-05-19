from random import choices, randint, randrange, random
    
# Generates a list with the genes, for example [0, 1, 0 ,0 ,1, 0. . .]
def generate_genome(length: int):
    return choices([0, 1], k=length)
    
# Create a population represented with a lot of genomes
def generate_population(size: int, genome_length: int):
    return [generate_genome(genome_length) for _ in range(size)]

# Create two children from genome dad & genome mum
def single_point_crossover(a, b):
    if len(a) != len(b):
        raise ValueError("Genomes a and b must be of same length")
    length = len(a)
    if length < 2:
        return a, b

    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]
    
# Mutates the genome 'num' times (after reproduction) to add diversity
def mutation(genome, num: int = 1, probability: float = 0.5):
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)
    return genome

# Calculates the total aptitude of all the population
def population_fitness(population, fitness_func):
    return sum([fitness_func(genome) for genome in population])
    
# Select two genomes for reproduction, based in their aptitude points.
# But, there are not guarantee that the selected are the betters.)
def selection_pair(population, fitness_func):
    return choices(
        population = population,
        weights=[fitness_func(genome) for genome in population],
        k=2
    )

# Generates a population sorted by aptitude (the best first)
def sort_population(population, fitness_func):
    return sorted(population, key=fitness_func, reverse=True)
    
def genome_to_string(genome):
    return "".join(map(str, genome))

# Run a simulation, with the typical process:
# Calculating aptitude for all -> selecting mates -> reproduction -> mutation
def run_evolution(
    populate_func, fitness_func, fitness_limit: int,
    selection_func, crossover_func, mutation_func, generation_limit: int = 100,
):
    population = populate_func()

    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = population[0:2]

        for _ in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

            population = next_generation

    return population, i