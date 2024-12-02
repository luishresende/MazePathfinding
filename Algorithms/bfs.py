from collections import deque

from Game import terrains, TerrainType

def bfs(graph, starting, objective):
    queue = deque([(starting, 0, [])]) # Fila: (nó atual, custo acumulado, caminho percorrido)
    visited = set()

    while queue:
        current, cost, path = queue.popleft()

        if current in visited:
            continue

        visited.add(current)
        new_path = path + [current]

        # Verifica se encontrou o objetivo
        if current == objective:
            return new_path, cost

        x, y = current
        current_node = graph[x][y] # Acessando o objeto grafo

        for adj in current_node.adjacents:
            terrain_index = terrains.index(adj.terrain_type)
            neighbour = (adj.matrix_position_x, adj.matrix_position_y)
            if neighbour not in visited:
                queue.append((neighbour, cost + terrain_index, new_path + [neighbour]))

    return None, None