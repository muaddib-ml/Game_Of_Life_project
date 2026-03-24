import random

class GameOfLife:
    def __init__(self, size):
        self.size = size
        self.matrix = self._initialize_matrix()
        self.random_fill()
        
    def _initialize_matrix(self):
        row = self.size
        matrix = []
        for i in range(self.size):
            col = [0] * row
            matrix.append(col)
        return matrix
    
    def random_fill(self):
        for i in range(self.size):
            for j in range(self.size):
                self.matrix[i][j] = random.randint(0, 1)
               
    def count_neighbor(self):
        neighbor_matrix = self._initialize_matrix()
        for i in range(self.size):
            for j in range(self.size):
                count = 0
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        if di == 0 and dj == 0:
                            continue
                        v_row = i + di
                        v_col = j + dj
                        if 0 <= v_row < self.size and 0 <= v_col < self.size:
                            if self.matrix[v_row][v_col] == 1:
                                count += 1
                neighbor_matrix[i][j] = count
        return neighbor_matrix
        
    def update_matrix(self, score_matrix):
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] == 0:
                    if score_matrix[i][j] == 3:
                        self.matrix[i][j] = 1
                elif self.matrix[i][j] == 1:
                    if score_matrix[i][j] == 2 or score_matrix[i][j] == 3:
                        continue
                    else:
                        self.matrix[i][j] = 0
        return self.matrix
    
    def print_matrix(self):
        for i in range(self.size):
            for j in range(self.size):
                print(f"{self.matrix[i][j]} ", end='')
            
            print()
        print()
