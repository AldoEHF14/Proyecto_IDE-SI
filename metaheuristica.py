import random as rndm
import time
import matplotlib.pyplot as plt

# Parte 1: Definiendo Genes y Cromosomas

def make_gene(initial=None):
    if initial is None:
        initial = [0] * 9
    mapp = {}
    gene = list(range(1, 10))
    rndm.shuffle(gene)
    for i in range(9):
        mapp[gene[i]] = i
    for i in range(9):
        if initial[i] != 0 and gene[i] != initial[i]:
            temp = gene[i], gene[mapp[initial[i]]]
            gene[mapp[initial[i]]], gene[i] = temp
            mapp[initial[i]], mapp[temp[0]] = i, mapp[initial[i]]
    return gene

def make_chromosome(initial=None):
    if initial is None:
        initial = [[0] * 9] * 9
    chromosome = []
    for i in range(9):
        chromosome.append(make_gene(initial[i]))
    return chromosome

# Parte 2: Creando la Primera Generación

def make_population(count, initial=None):
    if initial is None:
        initial = [[0] * 9] * 9
    population = []
    for _ in range(count):
        population.append(make_chromosome(initial))
    return population

# Parte 3: Función de Fitness

def get_fitness(chromosome):
    fitness = 0
    for i in range(9): 
        seen = {}
        for j in range(9): 
            if chromosome[j][i] in seen:
                seen[chromosome[j][i]] += 1
            else:
                seen[chromosome[j][i]] = 1
        for key in seen: 
            fitness -= (seen[key] - 1)
    for m in range(3): 
        for n in range(3):
            seen = {}
            for i in range(3 * n, 3 * (n + 1)):  
                for j in range(3 * m, 3 * (m + 1)):
                    if chromosome[j][i] in seen:
                        seen[chromosome[j][i]] += 1
                    else:
                        seen[chromosome[j][i]] = 1
            for key in seen: 
                fitness -= (seen[key] - 1)
    return fitness

# Parte 4: Cruzamiento y Mutación

def crossover(ch1, ch2):
    new_child_1 = []
    new_child_2 = []
    for i in range(9):
        x = rndm.randint(0, 1)
        if x == 1:
            new_child_1.append(ch1[i])
            new_child_2.append(ch2[i])
        elif x == 0:
            new_child_2.append(ch1[i])
            new_child_1.append(ch2[i])
    return new_child_1, new_child_2

def mutation(ch, pm, initial):
    for i in range(9):
        x = rndm.randint(0, 100)
        if x < pm * 100:
            ch[i] = make_gene(initial[i])
    return ch

# Parte 5: Implementando el Algoritmo Genético

def read_puzzle(address):
    puzzle = []
    f = open(address, 'r')
    for row in f:
        temp = row.split()
        puzzle.append([int(c) for c in temp])
    return puzzle

def r_get_mating_pool(population):
    fitness_list = []
    pool = []
    for chromosome in population:
        fitness = get_fitness(chromosome)
        fitness_list.append((fitness, chromosome))
    fitness_list.sort()
    weight = list(range(1, len(fitness_list) + 1))
    for _ in range(len(population)):
        ch = rndm.choices(fitness_list, weight)[0]
        pool.append(ch[1])
    return pool

def get_offsprings(population, initial, pm, pc):
    new_pool = []
    i = 0
    while i < len(population):
        ch1 = population[i]
        ch2 = population[(i + 1) % len(population)]
        x = rndm.randint(0, 100)
        if x < pc * 100:
            ch1, ch2 = crossover(ch1, ch2)
        new_pool.append(mutation(ch1, pm, initial))
        new_pool.append(mutation(ch2, pm, initial))
        i += 2
    return new_pool

# Parámetros del algoritmo
POPULATION = 1000
REPETITION = 1000
PM = 0.1
PC = 0.95

def genetic_algorithm(initial_file):
    initial = read_puzzle(initial_file)
    population = make_population(POPULATION, initial)
    for _ in range(REPETITION):
        mating_pool = r_get_mating_pool(population)
        rndm.shuffle(mating_pool)
        population = get_offsprings(mating_pool, initial, PM, PC)
        fit = [get_fitness(c) for c in population]
        m = max(fit)
        if m == 0:
            return population
    return population

# Ejecutar el algoritmo y generar el diagrama de caja y bigotes
tic = time.time()
r = genetic_algorithm("sudoku.txt")
toc = time.time()
print("Tiempo de ejecución:", toc - tic)

# Obtener los valores de fitness para graficar
fit = [get_fitness(c) for c in r]

# Generar el diagrama de caja y bigotes
plt.figure(figsize=(8, 6))
plt.boxplot(fit)
plt.title('Diagrama de Caja y Bigotes de Fitness')
plt.ylabel('Fitness')
plt.show()

# Imprimir el cromosoma con el mayor fitness
m = max(fit)
for c in r:
    if get_fitness(c) == m:
        for i in range(9):
            for j in range(9):
                print(c[i][j], end=" ")
            print("")
        break
