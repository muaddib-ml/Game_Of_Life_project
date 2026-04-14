"""
Logic module for the Game of Life simulation.

This module contains the GameOfLife class which handles the grid initialization,
neighbor counting, and state updates based on Conway's rules.
"""
import random


DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class GameOfLife:
    """
    An implementation of Conway's Game of Life on a square grid.

    This class manages a cellular automaton simulation where each cell
    is either alive (1) or dead (0), evolving based on its neighboring cells.

    Attributes:
        size (int): The dimension of one side of the square grid.
        matrix (list[list[int]]): The current state of the grid.
    """

    def __init__(self, size: int):
        """
        Initializes the simulation with a random starting state.

        Args:
            size (int): The size of the grid (size x size).
        """
        self.size = size
        self.matrix = self._initialize_matrix()
        self.random_fill()

    def _initialize_matrix(self) -> list[list[int]]:
        """
        Creates a square matrix filled with zeros.

        Returns:
            list[list[int]]: A 2D list of dimensions size x size, all set to 0.
        """
        return [[0] * self.size for _ in range(self.size)]

    def random_fill(self):
        """
        Populates the grid randomly with 0s and 1s.
        """
        for i in range(self.size):
            for j in range(self.size):
                self.matrix[i][j] = random.randint(0, 1)

    def step(self, wrap: bool):
        """
        Executes one full iteration of the Game of Life.

        Args:
            wrap (bool): If True, the grid wraps around its edges (toroidal topology).
                         If False, cells outside the boundary are treated as dead.
        """
        neighbor_counts = self._compute_scores_wrap() if wrap else self._compute_scores_boundary()
        self._update_matrix(neighbor_counts)

    def _compute_scores_boundary(self) -> list[list[int]]:
        """
        Calculates the number of live neighbors for each cell,
        treating out-of-bounds positions as dead (no wrapping).

        Returns:
            list[list[int]]: A 2D list of neighbor counts for each cell.
        """
        neighbor_counts = self._initialize_matrix()
        for i in range(self.size):
            for j in range(self.size):
                count = 0
                for di, dj in DIRECTIONS:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < self.size and 0 <= nj < self.size:
                        count += self.matrix[ni][nj]
                neighbor_counts[i][j] = count
        return neighbor_counts

    def _compute_scores_wrap(self) -> list[list[int]]:
        """
        Calculates the number of live neighbors for each cell,
        wrapping around the grid edges (toroidal topology).

        Returns:
            list[list[int]]: A 2D list of neighbor counts for each cell.
        """
        neighbor_counts = self._initialize_matrix()
        for i in range(self.size):
            for j in range(self.size):
                count = 0
                for di, dj in DIRECTIONS:
                    ni, nj = (i + di) % self.size, (j + dj) % self.size
                    count += self.matrix[ni][nj]
                neighbor_counts[i][j] = count
        return neighbor_counts

    def _update_matrix(self, neighbor_counts: list[list[int]]):
        """
        Applies Conway's rules to compute the next generation.

        Rules:
            - A live cell with 2 or 3 live neighbors survives.
            - A dead cell with exactly 3 live neighbors becomes alive.
            - All other cells die or remain dead.

        Args:
            neighbor_counts (list[list[int]]): The neighbor count matrix.
        """
        new_matrix = self._initialize_matrix()
        for i in range(self.size):
            for j in range(self.size):
                alive = self.matrix[i][j] == 1
                neighbors = neighbor_counts[i][j]
                if (alive and neighbors in (2, 3)) or (not alive and neighbors == 3):
                    new_matrix[i][j] = 1
        self.matrix = new_matrix

    def reset(self):
        """
        Resets the grid to an empty state (all cells dead).
        """
        self.matrix = self._initialize_matrix()

    def place_pattern(self, pattern_coords: list[tuple[int, int]], start_row: int, start_col: int):
        """
        Places a pattern on the grid at a given origin point.

        Cells outside the grid boundaries are silently ignored.

        Args:
            pattern_coords (list[tuple[int, int]]): List of (row, col) offsets relative to the origin.
            start_row (int): Row index of the placement origin.
            start_col (int): Column index of the placement origin.
        """
        for dr, dc in pattern_coords:
            nr, nc = start_row + dr, start_col + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                self.matrix[nr][nc] = 1
