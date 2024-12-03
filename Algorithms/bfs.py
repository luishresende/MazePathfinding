from collections import deque
from queue import Queue

from Game import terrains, TerrainType, Graph

def bfs(starting, objective, graph):
    """
    Realiza a busca em largura (BFS) a partir da posição inicial até a posição objetivo.

    Args:
        starting (tuple): Posição inicial (x, y).
        objective (tuple): Posição objetivo (x, y).

    Returns:
        path (list): Lista de posições que formam o caminho encontrado.
        cost (int): Custo total do caminho encontrado.
    """
    # Fila de BFS: (nó atual, custo acumulado, caminho percorrido)
    queue = deque([(starting, 0, [])])
    visited = set()
    # print(f"Objetivo a ser alcançado: {objective}")

    while queue:
        current, cost, path = queue.popleft()
        # print(f"Atual: {current}")

        # Se o nó já foi visitado, ignore
        if current in visited:
            continue

        # Marque o nó como visitado
        visited.add(current)
        new_path = path + [current]

        # Verifica se encontrou o objetivo
        if current == objective:
            # print(f"Caminho encontrado: {new_path} com custo {cost}")
            return new_path, cost

        x, y = current

        # Itera sobre os nós adjacentes
        for adj in graph[x][y].adjacents:
            # adj_x, adj_y = adj.matrix_position_x, adj.matrix_position_y

            # Se for uma parede, ignora
            if graph[adj.matrix_position_x][adj.matrix_position_y] == 0:
                continue

            # Calcula o custo baseado no tipo de terreno
            terrain_index = terrains.index(adj.terrain_type)
            neighbour = (adj.matrix_position_x, adj.matrix_position_y)

            if neighbour not in visited:
                # Atualiza o custo com base no tipo de terreno
                neighbour_cost = cost + terrain_index
                queue.append((neighbour, neighbour_cost, new_path + [neighbour]))

    return None, None  # Caso não encontre um caminho