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
                if i == 0:
                    if j == 0:
                        neighbor_matrix[i][j] = self.matrix[i+1][j] + self.matrix[i][j+1] + self.matrix[i+1][j+1]
                    elif j == self.size-1:
                        neighbor_matrix[i][j] = self.matrix[i+1][j] + self.matrix[i][j-1] + self.matrix[i+1][j-1]
                    else:
                        neighbor_matrix[i][j] = self.matrix[i+1][j] + self.matrix[i][j+1] + self.matrix[i+1][j+1] + self.matrix[i][j-1]  + self.matrix[i+1][j-1]
                elif i == self.size-1:
                    if j == 0:
                        neighbor_matrix[i][j] = self.matrix[i-1][j] + self.matrix[i][j+1] + self.matrix[i-1][j+1]
                    elif j == self.size-1:
                        neighbor_matrix[i][j] = self.matrix[i-1][j] + self.matrix[i][j-1] + self.matrix[i-1][j-1]
                    else:
                        neighbor_matrix[i][j] = self.matrix[i][j+1] + self.matrix[i][j-1] + self.matrix[i-1][j-1] + self.matrix[i-1][j]  + self.matrix[i-1][j+1]
                elif j == 0:
                    if i > 0 and i < self.size-1:
                        neighbor_matrix[i][j] = self.matrix[i+1][j] + self.matrix[i][j+1] + self.matrix[i+1][j+1] + self.matrix[i-1][j]  + self.matrix[i-1][j+1]
                elif j == self.size-1:
                    if i > 0 and i < self.size-1:
                        neighbor_matrix[i][j] = self.matrix[i-1][j] + self.matrix[i][j-1] + self.matrix[i-1][j-1] + self.matrix[i+1][j-1] + self.matrix[i+1][j]
                else:
                    neighbor_matrix[i][j] = self.matrix[i-1][j] + self.matrix[i][j-1] + self.matrix[i-1][j-1] + self.matrix[i-1][j+1]  + self.matrix[i][j+1] + self.matrix[i+1][j+1] + self.matrix[i+1][j] + self.matrix[i+1][j-1]
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
