import heapq
from Algorithms import heuristic
from Game.GameFunctions import update_maze_surface_algorithm, format_time
from time import sleep, time
from Game import algorithm_sleep_time

def greedy_search(start_node, target_pos, surface_manager, game_matrix, weights=(7.5, 1, 5)):
    visited = set()
    counter = 0
    iterations = 0
    start_time = time()
    priority_queue = [(heuristic.heuristic(start_node, target_pos, weights=weights), counter, start_node, [start_node])]  # (heurística, contador, nó atual, caminho)


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
            end_time = time()
            exec_time = end_time - start_time
            exec_time -= iterations * algorithm_sleep_time
            for node in path:
                surface_manager.update_surface(
                    update_maze_surface_algorithm,
                    graph=node,  # Passa cada nó individualmente
                    color=(0, 255, 0),
                    maze_square_size=15,
                )
            print(f"Busca Gulosa: {format_time(exec_time)}")
            return path

        # Adiciona os vizinhos à fila de prioridade
        for adjacent in current_node.adjacents:
            if adjacent not in visited:
                # print("Adicionando vizinho:", (adjacent.matrix_position_x, adjacent.matrix_position_y))
                counter += 1
                heapq.heappush(priority_queue, (heuristic.heuristic(adjacent, target_pos, weights=weights), counter, adjacent, path + [adjacent]))
        sleep(algorithm_sleep_time)
    end_time = time()
    exec_time = end_time - start_time
    exec_time -= iterations * algorithm_sleep_time
    print(f"Busca Gulosa: {format_time(exec_time)}")
    return None
