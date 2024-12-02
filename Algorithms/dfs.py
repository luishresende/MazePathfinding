from Game import terrains

def dfs(graph, starting, objective):
    stack = [(starting, 0, [])] # Pilha: (nó atual, custo acumulado, caminho percorrido)
    visited = set()

    while stack:
        current, cost, path = stack.pop()
        if current in visited:
            continue

        visited.add(current)
        new_path = path + [current]

        # Verifica se encontrou o objetivo
        if current == objective:
            return new_path, cost

        # Adiciona vizinhos à pilha
        for neighbor, terrain, reward in reversed(graph[current]): # Ordem reversa para manter a prioridade
            terrain_index = terrains.index(terrain)
            if neighbor not in visited:
                stack.append((neighbor, cost + terrains[terrain_index].default_coast, new_path))

    return None, None