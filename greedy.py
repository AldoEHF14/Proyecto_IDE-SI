#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from collections import OrderedDict
from colorama import init, Fore
import numpy as np
import time

init(autoreset=True)

class Sudoku(object):
    """
    Sudoku(values)

    A class for a Sudoku puzzle.

    Arguments:
    * values   -- a list containing the 81 values of a puzzle horizontally

    Instance variables:
    * values   -- a list containing the 81 values of a puzzle horizontally
    * rows     -- a two-dimensional list that stores 9 rows as lists, each
                  holding 9 values
    * columns  -- a two-dimensional list that stores 9 columns as lists, each
                  holding 9 values
    * squares  -- a two-dimensional list that stores 9 3x3 squares as lists,
                  each holding 9 values

    Returns an instance of the Sudoku class.
    """
    values = []
    rows = [[], [], [], [], [], [], [], [], []]
    columns = [[], [], [], [], [], [], [], [], []]
    squares = []
    grid = OrderedDict()

    def __init__(self, values):
        """See class docstring for details."""
        self.values = values

    def parse_sudoku(self, v, grid=True):
        """
        parse_sudoku(v, grid)

        Calls the parse methods for converting the values into lists.

        Arguments:
        * v     -- a list containing the 81 values of a puzzle horizontally
        * grid  -- a boolean which determines if parse_grid() is run (defaults
                   to True)
        """
        v = list(v)

        self.values = v
        self.rows = [[], [], [], [], [], [], [], [], []]
        self.columns = [[], [], [], [], [], [], [], [], []]
        self.squares = []

        self.parse_rows(v)
        self.parse_columns()
        self.parse_squares()
        if grid:
            self.parse_grid(v)

    def parse_rows(self, v):
        """
        parse_rows(v)

        Parses the values into the rows list.

        Arguments:
        * v  -- a list containing the 81 values of a puzzle horizontally
        """
        for i in range(9):
            for j in v[i * 9:i * 9 + 9]:
                if type(j) is int:
                    self.rows[i].append(j)
                else:
                    self.rows[i].append(0)

    def parse_columns(self):
        """
        parse_columns()

        Parses the rows into the columns list.
        """
        for row in self.rows:
            for i in range(9):
                self.columns[i].append(row[i])

    def parse_squares(self):
        """
        parse_squares()

        Parses the rows into the squares list.
        """
        for square_x in range(0, 7)[::3]:
            for square_y in range(0, 7)[::3]:
                square = []
                for x in range(3):
                    for y in range(3):
                        square.append(self.rows[square_x + x][square_y + y])

                self.squares.append(square)

    def parse_grid(self, v):
        """
        parse_grid(v)

        Parses the values into the grid dict.

        Arguments:
        * v  -- a list containing the 81 values of a puzzle horizontally
        """
        j = 0

        for l in 'ABCDEFGHI':
            for i in range(1, 10):
                self.grid[l + str(i)] = v[j]
                j += 1

    def locate_cell(self, cell):
        """
        locate_cell(cell)

        Given a cell index, returns the units the cell is in.

        Arguments:
        * cell      -- a string containing the index of a puzzle cell

        Returns:
        * location  -- a list containing the units the given cell is in
        """
        location = []
        x = int(cell[1]) - 1
        y = ord(cell[0]) - 65

        location.append(self.rows[y])
        location.append(self.columns[x])

        if y in range(3):
            if x in range(3):
                location.append(self.squares[0])
            elif x in range(3, 6):
                location.append(self.squares[1])
            elif x in range(6, 9):
                location.append(self.squares[2])
        elif y in range(3, 6):
            if x in range(3):
                location.append(self.squares[3])
            elif x in range(3, 6):
                location.append(self.squares[4])
            elif x in range(6, 9):
                location.append(self.squares[5])
        elif y in range(6, 9):
            if x in range(3):
                location.append(self.squares[6])
            elif x in range(3, 6):
                location.append(self.squares[7])
            elif x in range(6, 9):
                location.append(self.squares[8])

        return location

    def calculate_possibilities(self):
        """
        calculate_possibilities()

        For each empty cell, find numbers that are not in its units.

        Returns:
        * did_something  -- a boolean which stores if the function made any
                            changes to a cell
        """
        did_something = False
        print("Calculating possibilities...")

        for key, value in self.grid.items():
            if value == 0 or type(value) is list:
                self.grid[key] = []
                location = self.locate_cell(key)

                for i in range(1, 10):
                    if (i not in location[0] and i not in location[1] and i
                            not in location[2]):
                        self.grid[key].append(i)

                if len(self.grid[key]) == 1:
                    self.grid[key] = self.grid[key][0]
                    did_something = True

        return did_something

    def solve(self):
        """
        solve()

        Calculates all possibilities and continuously narrows them down.
        """
        while True:
            did_something = self.calculate_possibilities()
            self.parse_sudoku(self.grid.values(), grid=False)
            if not did_something:
                break

    @staticmethod
    def format(v):
        """
        format(v)

        Format a sudoku puzzle.

        Arguments:
        * v       -- a list containing the 81 values of a puzzle horizontally

        Returns:
        * result  -- a string that is a visually formatted version of the
                     values.
        """
        for key, value in enumerate(v):
            if value == 0 or type(value) == list:
                v[key] = ' '
                result = Fore.RED + ''
            else:
                result = Fore.GREEN + ''

        result += (' {}  {}  {} | {}  {}  {} | {}  {}  {}\n' +
                   ' {}  {}  {} | {}  {}  {} | {}  {}  {}\n' +
                   ' {}  {}  {} | {}  {}  {} | {}  {}  {}\n' +
                   ' --------+---------+--------\n' +
                   ' {}  {}  {} | {}  {}  {} | {}  {}  {}\n' +
                   ' {}  {}  {} | {}  {}  {} | {}  {}  {}\n' +
                   ' {}  {}  {} | {}  {}  {} | {}  {}  {}\n' +
                   ' --------+---------+--------\n' +
                   ' {}  {}  {} | {}  {}  {} | {}  {}  {}\n' +
                   ' {}  {}  {} | {}  {}  {} | {}  {}  {}\n' +
                   ' {}  {}  {} | {}  {}  {} | {}  {}  {}\n')
        result = result.format(*v)

        return result

easy_values = [
    5, 3, 0, 0, 7, 0, 0, 0, 0,
    6, 0, 0, 1, 9, 5, 0, 0, 0,
    0, 9, 8, 0, 0, 0, 0, 6, 0,
    8, 0, 0, 0, 6, 0, 0, 0, 3,
    4, 0, 0, 8, 0, 3, 0, 0, 1,
    7, 0, 0, 0, 2, 0, 0, 0, 6,
    0, 6, 0, 0, 0, 0, 2, 8, 0,
    0, 0, 0, 4, 1, 9, 0, 0, 5,
    0, 0, 0, 0, 8, 0, 0, 7, 9
]

def generar_diagramas(sudoku_values):
    # Convertir los valores del Sudoku en un array de NumPy de 9x9
    sudoku_array = np.array(sudoku_values).reshape((9, 9))

    # Crear una figura y ejes para el diagrama de caja y brazos
    fig, ax = plt.subplots()

    # Crear el diagrama de caja y brazos
    ax.boxplot(sudoku_array, patch_artist=True)

    # Configurar las etiquetas de los ejes
    ax.set_xticklabels([str(i) for i in range(1, 10)])
    ax.set_yticklabels([str(i) for i in range(1, 10)])

    # Añadir título y etiquetas de los ejes
    ax.set_title('Diagrama de Caja y Brazos del Sudoku')
    ax.set_xlabel('Columnas')
    ax.set_ylabel('Valores')

    # Mostrar el diagrama de caja y brazos
    plt.show()

def main():
    """
    main()

    Función principal que crea un objeto Sudoku y muestra la solución.
    """
    print(Fore.BLUE + '\nSudoku Solver\n=============\n')

    sudoku = Sudoku(easy_values)
    sudoku.parse_sudoku(easy_values)

    # Medir el tiempo de inicio
    start_time = time.time()

    sudoku.solve()

    # Medir el tiempo de finalización
    end_time = time.time()

    print('\n')
    print(sudoku.format(easy_values))
    print(" ->\n")
    print(sudoku.format(sudoku.values))

    generar_diagramas(sudoku.values)

    # Calcular el tiempo transcurrido
    elapsed_time = end_time - start_time
    print("Tiempo transcurrido:", elapsed_time, "segundos")

if __name__ == '__main__':
    main()