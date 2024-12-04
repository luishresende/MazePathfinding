import heapq
from Game import terrains
from Algorithms import heuristic
from Game.GameFunctions import update_maze_surface_algorithm
from time import sleep


def search_star(start_node, target_pos, surface_manager, game_matrix):
    visited = set()
    counter = 0
    priority_queue = [(0 + heuristic.heuristic(start_node, target_pos), counter, start_node, 0, [start_node])]

    while priority_queue:
        _, _, current_node, coast, path = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)
        surface_manager.update_surface(
            update_maze_surface_algorithm,
            graph=current_node,
            color=(255, 0, 0),
            maze_square_size=15,
        )

        # Verifica se encontrou o objetivo
        if (current_node.matrix_position_x, current_node.matrix_position_y) == target_pos:
            for node in path:
                surface_manager.update_surface(
                    update_maze_surface_algorithm,
                    graph=node,  # Passa cada nó individualmente
                    color=(0, 255, 0),
                    maze_square_size=15,
                )
            return path

        # Adiciona vizinhos a fila de prioridade
        for adjacent in current_node.adjacents:
            terrain_index = terrains.index(adjacent.terrain_type)
            if adjacent not in visited:
                g = coast + terrains[terrain_index].default_coast
                f = g + heuristic.heuristic(adjacent, target_pos)
                counter += 1
                heapq.heappush(priority_queue, (f, counter, adjacent, g, path + [adjacent]))
        sleep(0.02)
    return None, None