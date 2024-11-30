class Graph:
    def __init__(self, terrain_type, matrix_position_x, matrix_position_y, reward=False):
        self.terrain_type = terrain_type
        self.matrix_position_x = matrix_position_x
        self.matrix_position_y = matrix_position_y
        self.reward = reward
        self.adjacents = []

    def add_adjacent(self, adj):
        self.adjacents.append(adj)
