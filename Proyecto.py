import numpy as np
import random
import sys
import time
import matplotlib.pyplot as plt


# Función fitness actualizada para trabajar con diferentes tamaños de Sudoku
def function_fitness(board):
    size = len(board)
    subgrid_size = int(size ** 0.5)  # Tamaño de las subgrillas
    fitness = 0
    
    # Evaluar cada fila
    for i in range(size):
        row_values = board[i]
        # Calcular los valores únicos en la fila
        unique_row_values = set(row_values)
        # Calcular la cantidad de valores únicos y restarlos del tamaño de la fila
        unique_row_count = len(unique_row_values)
        fitness += size - unique_row_count

        #cuenta los ceros (casillas vacias) por cada fila y los cuenta como errores
        cuenta0 = np.count_nonzero(row_values == 0)
        fitness += cuenta0
    
    # Evaluar cada columna
    for i in range(size):
        column_values = [board[j][i] for j in range(size)]
        # Calcular los valores únicos en la columna
        unique_column_values = set(column_values)
        # Calcular la cantidad de valores únicos y restarlos del tamaño de la columna
        unique_column_count = len(unique_column_values)
        fitness += size - unique_column_count
    
    # Evaluar cada submatriz
    for i in range(size):
        for j in range(size):
            subgrid_values = [board[i // subgrid_size * subgrid_size + k][j // subgrid_size * subgrid_size + l]
                              for k in range(subgrid_size) for l in range(subgrid_size)]
            # Calcular los valores únicos en la subseccion
            unique_subgrid_values = set(subgrid_values)
            # Calcular la cantidad de valores únicos y restarlos del tamaño de la submatriz
            unique_subgrid_count = len(unique_subgrid_values)
            fitness += size - unique_subgrid_count
    
    return fitness


def validar_sudoku(board, row, col, num):
    size = len(board)
    subgrid_size = int(size ** 0.5)  # Tamaño de las subgmatriz

    # Verifica si es válido colocar 'num' en la posición (row, col) del tablero
    # Verifica la fila
    if num in board[row]:
        return False

    # # Verifica la columna
    column_values = []
    for i in range(size):
        column_values.append(board[i][col])

    if num in column_values:
        return False

    # Verifica la submatriz
    startRow, startCol = subgrid_size * (row // subgrid_size), subgrid_size * (col // subgrid_size)
    for i in range(startRow, startRow + subgrid_size):
        for j in range(startCol, startCol + subgrid_size):
            if board[i][j] == num:
                return False

    return True

def generar_sudoku_inicial(particle,size, board):
    #sudoku_inicial = [[0] * size for _ in range(size)]
    sudoku_inicial = particle
    subgrid_size = int(size ** 0.5)  # Tamaño de las subgmatriz

    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                possible_values = [n for n in range(1, size + 1)]
                random.shuffle(possible_values)
                for value in possible_values:
                    if validar_sudoku(sudoku_inicial, i, j, value):
                        sudoku_inicial[i][j] = value
                        break

    return sudoku_inicial

def PSO(sudoku_matriz, size, num_iterations, num_particles):
    # Establecer la semilla
    random.seed(123)
    c1=1
    c2=1
    rand=0.3
    board = leer_archivo(sudoku_matriz, size)
    subgrid_size = int(size ** 0.5)  # Tamaño de las submatrices

    particles = []
    global_best_board = None
    global_best_fitness = float('inf')

    # Inicializar partículas con soluciones aleatorias
    for _ in range(num_particles):
        particle = np.copy(board)
        particle = generar_sudoku_inicial(particle,size, board)
        particles.append(particle)

    Pbest = np.copy(particles)
    Pbest_fitness = np.array([function_fitness(p) for p in Pbest])

    best_index = np.argmin(Pbest_fitness)
    global_best_board = np.copy(Pbest[best_index])
    global_best_fitness = np.min(Pbest_fitness)

    #imprimir_mejor_solucion((p for p in Pbest), 1)
    #print(pbest_fitness)

    start_time = time.time()

    for iteration in range(1, num_iterations + 1):
        k=0
    
        for particula in particles:
            # Actualización de la velocidad y posición de la partícula
            v = rand * (c1 * np.random.rand() * (Pbest[k] - particula) + c2 * np.random.rand() * (global_best_board - particula))
            # Limitar la velocidad entre [-1, 1]
            
            #print(vl for vl in v)
            for vl in v:
                for i in range(len(vl)):
                    #print(f"{vc}\n")
                    if vl[i] <= -1:  
                        vl[i] = -1
                    elif vl[i] >= 1:
                        vl[i] = 1
                    else:
                        vl[i] = 0
            
            #print(v)
            #imprimir_mejor_solucion(particula, fitness)
            particula = particula + v
            fitness = function_fitness(particula)

            if fitness < Pbest_fitness[k]:
                print(fitness, Pbest_fitness[k],"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                #print(particle)
                Pbest[k] = np.copy(particle)
                #print(pbest)
                Pbest_fitness[k] = fitness

            imprimir_mejor_solucion(Pbest[k], Pbest_fitness[k])
            k+=1
        
        best_index = np.argmin(Pbest_fitness)
        global_best_board = np.copy(Pbest[best_index])
        global_best_fitness = np.min(Pbest_fitness)
        
        if global_best_fitness ==0:
            break

            
        print(f"////////////////////    {iteration}    //////////////////////////////// {global_best_fitness}")

        #print("Iteración:", iteration, "Mejor fitness:", global_best_fitness)

    end_time = time.time()

    print("Tiempo de ejecución:", end_time - start_time, "segundos")
    imprimir_mejor_solucion(global_best_board, global_best_fitness)
    return Pbest_fitness


def leer_archivo(nombre_archivo, tamMatriz):
    instancia = []

    with open(nombre_archivo, 'r') as archivo:
        for _ in range(tamMatriz):
            fila = list(map(int, archivo.readline().split()))
            instancia.append(fila)

    return instancia

def imprimir_mejor_solucion(sudoku_matriz, fitness):

    #print("-------- Mejor Solución encontrada del Sudoku ---------\n")

    for fila in sudoku_matriz:
        print("\t\t", fila)
    
    print(f"Fitness:{fitness}\n")




if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("Sintaxis: ee.py <Archivo> <tamaño> <número_iteraciones> <numero_particulas>")
    else:
        name=""
        resultados=[]
        for i in range(3):
            if i == 0:
                name="instanciaSudoku.txt"
            elif i==1:
                name = "instanciaSudoku2.txt"
            else:
                name = "instanciaSudoku3.txt"

            resultados.append(PSO(name, int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])))
            print("=====================================================================================================")


    fig, axs = plt.subplots(1, 3, figsize=(12, 4))


    print(resultados)
    axs[0].boxplot(resultados[0])
    axs[0].set_title("instanciaSudoku.txt")

    # Boxplot para z2 en el segundo subgráfico
    axs[1].boxplot(resultados[1])
    axs[1].set_title("instanciaSudoku2.txt")

    # Boxplot para z3 en el tercer subgráfico
    axs[2].boxplot(resultados[2])
    axs[2].set_title("instanciaSudoku3.txt")

    plt.show()