import heapq

from Algorithms import heuristic
from Game import terrains

def greedy_search(graph, starting, objective):
    priority_queue = [(heuristic.heuristic(starting, objective), starting, 0, [])] # (heuristica, nó atual, custo, caminho)
    visited = set()

    while priority_queue:
        _, current, cost, path = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)
        new_path = path + [current]

        # Verifica se encontrou o objetivo
        if current == objective:
            return new_path, cost

        x, y = current
        current_node = graph[x][y]

        # Adiciona vizinhos a fila de prioridade
        for adj in current_node.adjacents:
            terrain_index = terrains.index(adj.terrain_type)
            neighbour = (adj.matrix_position_x, adj.matrix_position_y)
            if neighbour not in visited:
                heapq.heappush(priority_queue, (heuristic.heuristic(neighbour, objective), neighbour, cost + terrains[terrain_index].default_coast, new_path))

    return None, None