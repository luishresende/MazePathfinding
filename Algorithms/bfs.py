from collections import deque
from Game import algorith_path_manager
from Game.GameFunctions import update_maze_surface_algorithm
from time import sleep


def bfs(start_node, target_pos, surface_manager, game_matrix):
    """
    Busca em largura para encontrar um nó com a posição (x, y) especificada e retorna o caminho.

    :param start_node: O nó inicial do grafo.
    :param target_pos: A posição alvo como uma tupla (x, y).
    :return: Uma lista de nós representando o caminho encontrado ou None se nenhum caminho for encontrado.
    """
    visited = set()  # Para rastrear os nós visitados
    queue = deque([(start_node, [start_node])])  # Fila para rastrear os nós e os caminhos

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
        print(f'Game Matrix[{current_node.matrix_position_x}][{current_node.matrix_position_y}]: {game_matrix[current_node.matrix_position_x][current_node.matrix_position_y]}')


        # Verifica se o nó atual está na posição alvo
        if (current_node.matrix_position_x, current_node.matrix_position_y) == target_pos:
            print(path)
            return path  # Retorna o caminho encontrado

        # Adiciona os nós adjacentes não visitados à fila, com o caminho atualizado
        for adjacent in current_node.adjacents:
            if adjacent not in visited:
                queue.append((adjacent, path + [adjacent]))
        sleep(0.3)
    return None  # Retorna None se nenhum nó na posição especificada for encontrado
