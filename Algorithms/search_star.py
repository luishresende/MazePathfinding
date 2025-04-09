from Algorithms.VetorOrdenadoAdjacente import VetorOrdenadoAdjacente
from Game import algorithm_sleep_time
from Algorithms import heuristic
from Game.GameFunctions import update_maze_surface_algorithm, format_time
from time import sleep, time


def search_star(start_node, target_pos, surface_manager, game_matrix, reward_value=1, weights=(7.5, 1, 5)):
    visited = set()
    back_tracking_coast = 20
    priority_queue = VetorOrdenadoAdjacente()

    start_time = time()
    iterations = 0
    # Adiciona o nó inicial à fila de prioridade
    initial_heuristic = heuristic.heuristic(start_node, target_pos, weights=weights)
    priority_queue.inserir(start_node, custo_g=0, heuristica=initial_heuristic, caminho=[start_node])

    while not priority_queue.is_empty():
        _, _, current_node, coast, path = priority_queue.get_primeiro()

        if current_node in visited:
            coast += back_tracking_coast

        visited.add(current_node)
        surface_manager.update_surface(
            update_maze_surface_algorithm,
            graph=current_node,
            color=(255, 0, 0),
            maze_square_size=15,
        )

        # Verifica se encontrou o objetivo
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

            print(f"Busca A*: {format_time(exec_time)}")
            return path

        # Adiciona vizinhos a fila de prioridade
        for adjacent in current_node.adjacents:
            if adjacent not in visited:
                g = coast + adjacent.terrain_type.default_coast
                f = g + heuristic.heuristic(adjacent, target_pos, weights=weights) #- 100 if adjacent.reward else 0

                priority_queue.inserir(adjacent, custo_g=g, heuristica=f, caminho=path + [adjacent])
        sleep(algorithm_sleep_time)
    end_time = time()
    exec_time = end_time - start_time
    exec_time -= iterations * algorithm_sleep_time
    print(f"Busca A*: {format_time(exec_time)}")
    return None