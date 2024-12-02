from collections import deque

from Game import terrains, TerrainType

def bfs(graph, starting, objective):
    queue = deque([(starting, 0, [])]) # Fila: (nó atual, custo acumulado, caminho percorrido)
    visited = set()

    while queue:
        current, cost, path = queue.popleft()

        current_tuple = tuple(current)
        if current_tuple in visited:
            continue

        visited.add(current_tuple)
        new_path = path + [current]

        # Verifica se encontrou o objetivo
        if current == objective:
            return new_path, cost
        print("Current Tuple", current_tuple)
        current_node = graph[current_tuple] # Acessando o objeto grafo
        print("Currente Node", current_node)
        for neighbor, terrain, reward in current_node.adjs_list:
            terrain_index = terrains.index(terrain)
            if neighbor not in visited:
                queue.append((neighbor, cost + terrain_index, new_path + [neighbor]))

    return None, None