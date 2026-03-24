import random


class GameOfLife:

    def __init__(self, size):
        self.size = size
        self.matrix = self._initialize_matrix()
        self.score_matrix = self._initialize_matrix()
        self.random_fill()

    def _initialize_matrix(self):
        row = self.size
        matrix = []
        for _ in range(self.size):
            col = [0] * row
            matrix.append(col)
        return matrix

    def random_fill(self):
        for i in range(self.size):
            for j in range(self.size):
                self.matrix[i][j] = random.randint(0, 1)

    def count_neighbor(self):
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
        for i in range(self.size):
            for j in range(self.size):
                print(f"{self.matrix[i][j]} ", end="")
            print()
        print()
