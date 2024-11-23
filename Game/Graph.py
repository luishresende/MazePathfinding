class Graph:
    adjs_list = []
    def __init__(self, terrain_type, matrix_position_x, matrix_position_y, reward=False):
        self.terrain_type = terrain_type
        self.matrix_position_x = matrix_position_x
        self.matrix_position_y = matrix_position_y
        self.reward = reward

    def add_adjacent(self, adj):
        self.adjs_list.append(adj)
