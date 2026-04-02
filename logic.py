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
    """

    def __init__(self, size):
        """
        Initializes the simulation with a random starting state.
 
        Args:
            size (int): The size of the grid (size x size).
        """
        self.size = size
        self.matrix = self._initialize_matrix()
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

    def step(self):
        """
        Executes one full iteration of the Game of Life.
 
        This method triggers the neighbor counting process and then
        updates the grid state based on the calculated scores.
        """
        neighbor_counts = self._compute_scores()
        self._update_matrix(neighbor_counts)

    def _compute_scores(self):
        """
        Calculates the number of living neighbors for every cell in the grid.

        It checks the 8 adjacent directions for each cell.

        Returns:
            list[list[int]]: A 2D list of neighbor counts for each cell.
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
        neighbor_counts = self._initialize_matrix()
        for i in range(self.size):
            for j in range(self.size):
                count = 0
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < self.size and 0 <= nj < self.size:
                        count += self.matrix[ni][nj]
                neighbor_counts[i][j] = count
        return neighbor_counts

    def _update_matrix(self, neighbor_counts):
        """
        Applies the Game of Life rules to update the grid state.
 
        Rules applied:
        1. Any dead cell with exactly 3 live neighbors becomes a live cell (Birth).
        2. Any live cell with 2 or 3 live neighbors survives to the next generation.
        3. All other live cells die (Overpopulation or Underpopulation).
        4. All other dead cells stay dead.
 
        Args:
            neighbor_counts (list[list[int]]): The neighbor count matrix from _compute_scores.
        """
        new_matrix = self._initialize_matrix()
        for i in range(self.size):
            for j in range(self.size):
                alive = self.matrix[i][j] == 1
                neighbors = neighbor_counts[i][j]
                if alive and neighbors in (2, 3):
                    new_matrix[i][j] = 1
                elif not alive and neighbors == 3:
                    new_matrix[i][j] = 1
        self.matrix = new_matrix
