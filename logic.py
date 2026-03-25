"""
Logic module for the Game of Life simulation.

This module contains the GameOfLife class which handles the grid initialization,
neighbor counting, and state updates based on Conway's rules.
"""
import random


class GameOfLife:
    """
    An implementation of Conway's Game of Life on a square grid.
    
    This class manages a cellular automaton simulation where each cell 
    is either alive (1) or dead (0), evolving based on its neighboring cells.

    Attributes:
        size (int): The dimension of one side of the square grid.
        matrix (list[list[int]]): The current state of the grid.
        score_matrix (list[list[int]]): An intermediate grid storing the 
            neighbor count for each cell.
    """
    def __init__(self, size):
        """
        Initializes the simulation with a random starting state.

        Args:
            size (int): The size of the grid (size x size).
        """
        self.size = size
        self.matrix = self._initialize_matrix()
        self.score_matrix = self._initialize_matrix()
        self.random_fill()

    def _initialize_matrix(self):
        """
        Creates a square matrix filled with zeros.

        Returns:
            list[list[int]]: A 2D list of dimensions self.size x self.size.
        """
        return [[0] * self.size for _ in range(self.size)]

    def random_fill(self):
        """
        Populates the main matrix randomly with 0s and 1s.
        """
        for i in range(self.size):
            for j in range(self.size):
                self.matrix[i][j] = random.randint(0, 1)

    def count_neighbor(self):
        """
        Calculates the number of living neighbors for every cell in the grid.
        
        It checks the 8 adjacent directions for each point and stores the 
        total count in `self.score_matrix`.
        """
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        for i in range(self.size):
            for j in range(self.size):
                count = 0
                for di, dj in directions:
                    v_row, v_col = i + di, j + dj
                    if 0 <= v_row < self.size and 0 <= v_col < self.size:
                        count += self.matrix[v_row][v_col]
                self.score_matrix[i][j] = count

    def update_matrix(self):
        """
        Applies the Game of Life rules to update the grid state.
        
        Rules applied:
        1. Any dead cell with exactly 3 live neighbors becomes a live cell (Birth).
        2. Any live cell with 2 or 3 live neighbors survives to the next generation.
        3. All other live cells die (Overpopulation or Underpopulation).
        4. All other dead cells stay dead.

        Returns:
            list[list[int]]: The updated matrix.
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] == 0:
                    if self.score_matrix[i][j] == 3:
                        self.matrix[i][j] = 1
                elif self.matrix[i][j] == 1:
                    if self.score_matrix[i][j] == 2 or self.score_matrix[i][j] == 3:
                        continue
                    self.matrix[i][j] = 0
        return self.matrix

    def print_matrix(self):
        """
        Prints the current grid state to the console.
        """
        for i in range(self.size):
            for j in range(self.size):
                print(f"{self.matrix[i][j]} ", end="")
            print()
        print()
