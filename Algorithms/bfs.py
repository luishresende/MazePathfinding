from collections import deque
from Game import algorithm_sleep_time
from Game.GameFunctions import update_maze_surface_algorithm, format_time
from time import sleep, time


def bfs(start_node, target_pos, surface_manager, game_matrix):
    """
    Busca em largura para encontrar um nó com a posição (x, y) especificada e retorna o caminho.

    :param start_node: O nó inicial do grafo.
    :param target_pos: A posição alvo como uma tupla (x, y).
    :return: Uma lista de nós representando o caminho encontrado ou None se nenhum caminho for encontrado.
    """
    iterations = 0
    visited = set()  # Para rastrear os nós visitados
    queue = deque([(start_node, [start_node])])  # Fila para rastrear os nós e os caminhos

    start_time = time()
    while queue:
        current_node, path = queue.popleft()  # Remove o nó da frente da fila e seu caminho

        # Verifica se já foi visitado
        if current_node in visited:
            continue

        # Marca como visitado
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
            print(f"Busca em Largura: {format_time(exec_time)}")
            return path  # Retorna o caminho encontrado

        # Adiciona os nós adjacentes não visitados à fila, com o caminho atualizado
        for adjacent in current_node.adjacents:
            if adjacent not in visited:
                queue.append((adjacent, path + [adjacent]))
        sleep(algorithm_sleep_time)
        iterations += 1
    end_time = time()
    exec_time = end_time - start_time
    exec_time -= iterations * algorithm_sleep_time
    print(f"Busca em Largura: {format_time(exec_time)}")
    return None  # Retorna None se nenhum nó na posição especificada for encontrado
