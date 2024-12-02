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

        x, y = current
        current_node = graph[x][y]

        # Adiciona vizinhos à pilha
        for adj in current_node.adjacents: # Ordem reversa para manter a prioridade
            terrain_index = terrains.index(adj.terrain_type)
            neighbor = (adj.matrix_position_x, adj.matrix_position_y)
            if neighbor not in visited:
                stack.append((neighbor, cost + terrain_index, new_path + [neighbor]))

    return None, None