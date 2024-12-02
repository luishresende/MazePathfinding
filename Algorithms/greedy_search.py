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

        # Adiciona vizinhos a fila de prioridade
        for neighbor, terrain, reward in graph[current]:
            terrain_index = terrains.index(terrain)
            if neighbor not in visited:
                heapq.heappush(priority_queue, (heuristic.heuristic(neighbor, objective), neighbor, cost + terrains[terrain_index].default_coast, new_path))

    return None, None