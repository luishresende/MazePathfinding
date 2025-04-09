from Game import algorithm_sleep_time
from Game.GameFunctions import update_maze_surface_algorithm, format_time
from time import sleep, time

def dfs(start_node, target_pos, surface_manager, game_matrix):
    visited = set()
    stack = [(start_node, [start_node])] # Pilha: (nó atual, caminho percorrido)
    start_time = time()
    iterations = 0
    while stack:
        current_node, path = stack.pop()

        if current_node in visited:
            continue

        visited.add(current_node)
        surface_manager.update_surface(
            update_maze_surface_algorithm,
            graph=current_node,
            color=(255, 0, 0),
            maze_square_size=15,
        )

        # Verifica se o nó atual está na posição alvo
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
            print(f"Busca em Profundidade: {format_time(exec_time)}")
            return path

        # Adiciona os nós adjacentes não visitados à fila, com o caminho atualizado
        for adjacent in current_node.adjacents:
            if adjacent not in visited:
                stack.append((adjacent, path + [adjacent]))
        sleep(algorithm_sleep_time)
        iterations += 1
    end_time = time()
    exec_time = end_time - start_time
    exec_time -= iterations * algorithm_sleep_time
    print(f"Busca em Profundidade: {format_time(exec_time)}")
    return None