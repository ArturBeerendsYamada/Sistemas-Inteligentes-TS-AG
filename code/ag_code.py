from random import randint, random, choices
import sys
import csv
import numpy as np

MAX_SIZE = sys.maxsize

# Number of cities 
city_amount = 15

# Name of the cties
genes = "ABCDEFGHIJKLMNO"

# Staring node for search
node_start = 0

# Size of initial population
population_size = 10

def process_csv(csv_path):
    
    matrix = []

    # Read the CSV file and build the matrix
    try:
        with open(csv_path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                matrix.append([int(value) for value in row])
            return matrix
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return


class individual:
    def __init__(self) -> None:
        # Path walked by salesman
        self.genome = ""
        # Fitness of path
        self.fitness = 0

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness


# Return a random number
# from start and end
def rand_num(start, end):
    return randint(start, end-1)

# Function to check if the character
# has already occurred in the string
def repeat(s, ch):
    for i in range(len(s)):
        if s[i] == ch:
            return True
    return False

# Function to return a mutated GNOME
# Mutated GNOME is a string
# with a random interchange
# of two genes to create variation in species
def mutation(gnome):
    gnome = list(gnome)
    while True:
        r = rand_num(1, city_amount)
        r1 = rand_num(1, city_amount)
        if r1 != r:
            temp = gnome[r]
            gnome[r] = gnome[r1]
            gnome[r1] = temp
            break
    return ''.join(gnome)


# Function to return a valid GNOME string
# required to create the population
def create_genome():
    gnome = "A"
    while True:
        if len(gnome) == city_amount:
            gnome += gnome[0]
            break
        temp = rand_num(1, city_amount)
        if not repeat(gnome, chr(temp + 65)):
            gnome += chr(temp + 65)

    return gnome


# Function to return the fitness value of a gnome.
# The fitness value is the path length
# of the path represented by the GNOME.
def cal_fitness(gnome, mp):

    f = 0

    for i in range(len(gnome) - 1):
        if mp[ord(gnome[i]) - 65][ord(gnome[i + 1]) - 65] == MAX_SIZE:
            return MAX_SIZE
        f += mp[ord(gnome[i]) - 65][ord(gnome[i + 1]) - 65]

    return f

def selection(population_size, fitness_scores):
    return(choices(range(population_size), weights=fitness_scores, k=2))

def crossover(genome1, genome2):

    gene1 = [ord(i)-65 for i in genome1]
    gene2 = [ord(i)-65 for i in genome2]

       
    values = np.random.choice(gene1, size=3, replace=False) # random choice of values to rearrange
        
    gene1_index = [i for i in range(len(gene1)) if gene1[i] in values] # list of array indices of where the values appear
    gene2_index = [i for i in range(len(gene1)) if gene2[i] in values]

    temp = [i for i in gene1 if i in values] # values in the order in which they appear in gene1
                        
    gene1[gene1_index[0]], gene1[gene1_index[1]], gene1[gene1_index[2]] = gene2[gene2_index[0]], gene2[gene2_index[1]], gene2[gene2_index[2]]
    gene2[gene2_index[0]], gene2[gene2_index[1]], gene2[gene2_index[2]] = temp[0], temp[1], temp[2]

    new_genome1 = ""
    new_genome2 = ""

    for j in gene1:
        new_genome1 += chr(j+65)
                                    
    for k in gene2:
        new_genome2 += chr(k+65)

    return new_genome1, new_genome2




def run_tsp(mp):

    # Starting generation
    generation = 1

    # Number of genetic iterations
    genetic_limit = 10

    # Crossover Threshold
    crossover_threshold = 0.8

    # Mutation Threshold
    mutation_threshold = 0.2

    population = []

    # Populate genome pool
    for i in range(population_size):

        temp = individual()
        temp.genome = create_genome()
        temp.fitness = cal_fitness(temp.genome, mp)
        population.append(temp)
    
    print("\nPopulação Inicial: \nGenoma     Fitness\n")

    for indiv in population:
        print(indiv.genome, indiv.fitness)

    fitness_scores = [indiv.fitness for indiv in population]

    order = np.array(sorted([*enumerate(fitness_scores)], key=lambda x: x[1], reverse=False), dtype=int)[:, 0] 
    population = [population[i] for i in order]
    fitness_scores = sorted(fitness_scores, reverse=False)

    while generation < genetic_limit:
        
        replaced = 1
        new_pop = population

        while replaced < population_size:

            index = selection(population_size, fitness_scores)
            
            child1 = individual()
            child2 = individual()

            # Crossover
            if random() < crossover_threshold:
                child1.genome, child2.genome = crossover(population[index[0]].genome, population[index[1]].genome)
            else:
                child1.genome, child2.genome = population[index[0]].genome, population[index[1]].genome

                
            # Mutation
            if random() < mutation_threshold:
                child1.genome = mutation(child1.genome)

            if random() < mutation_threshold:
                child2.genome = mutation(child2.genome)

            child1.fitness = cal_fitness(child1.genome, mp)
            new_pop[replaced] = child1
            replaced += 1
            if replaced < population_size:
    
                child2.fitness = cal_fitness(child2.genome, mp)
                new_pop[replaced] = child2 
                replaced += 1

        population = new_pop
        fitness_scores = [indiv.fitness for indiv in population]

        order = np.array(sorted([*enumerate(fitness_scores)], key=lambda x: x[1], reverse=False), dtype=int)[:, 0] 
        population = [population[i] for i in order]
        fitness_scores = sorted(fitness_scores, reverse=False)

        print("generation:", generation)
        print("Genome   Fitness")

        for indiv in population:
            print(indiv.genome, indiv.fitness)
        generation += 1
        

if __name__ == "__main__":

    # Read csv
    mp = process_csv("./input/matriz_size_15.csv") 

    run_tsp(mp)

    pass

