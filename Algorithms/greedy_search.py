import heapq
from Algorithms import heuristic
from Game.GameFunctions import update_maze_surface_algorithm
from time import sleep

def greedy_search(start_node, target_pos, surface_manager, game_matrix):
    print("\nIniciando busca gulosa:")
    visited = set()
    counter = 0
    priority_queue = [(heuristic.heuristic(start_node, target_pos), counter, start_node, [start_node])]  # (heurística, contador, nó atual, caminho)

    while priority_queue:
        # print("\nFronteira (fila de prioridade):")
        # print([(h[0], h[2].matrix_position_x, h[2].matrix_position_y) for h in priority_queue])  # Mostra o estado da fronteira

        _, _, current_node, path = heapq.heappop(priority_queue)

        # print("Atual:", (current_node.matrix_position_x, current_node.matrix_position_y))

        if current_node in visited:
            continue

        visited.add(current_node)
        surface_manager.update_surface(
            update_maze_surface_algorithm,
            graph=current_node,
            color=(255, 0, 0),
            maze_square_size=15,
        )

        # Verifica se o nó atual é o objetivo
        if (current_node.matrix_position_x, current_node.matrix_position_y) == target_pos:
            for node in path:
                surface_manager.update_surface(
                    update_maze_surface_algorithm,
                    graph=node,  # Passa cada nó individualmente
                    color=(0, 255, 0),
                    maze_square_size=15,
                )
            return path

        # Adiciona os vizinhos à fila de prioridade
        for adjacent in current_node.adjacents:
            if adjacent not in visited:
                # print("Adicionando vizinho:", (adjacent.matrix_position_x, adjacent.matrix_position_y))
                counter += 1
                heapq.heappush(priority_queue, (heuristic.heuristic(adjacent, target_pos), counter, adjacent, path + [adjacent]))
        sleep(0.02)

    print("Nenhum caminho encontrado.")
    return None
