import heapq
from Game import terrains
from Algorithms import heuristic

def search_star(graph, starting, objective):
    priority_queue = [(0 + heuristic.heuristic(starting, objective), starting, 0, [])] # (f(n), nó atual, custo, caminho)
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
        for neighbor, terrain, reward, in graph[current]:
            terrain_index = terrains.index(terrain)
            if neighbor not in visited:
                g = cost + terrains[terrain_index].default_coast
                f = g + heuristic.heuristic(neighbor, objective)
                heapq.heappush(priority_queue, (f, neighbor, g, new_path))

    return None, None