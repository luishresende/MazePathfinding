from Game.Graph import Graph
from Game import reward_image

import pygame

def initialize_graphs(graph_matrix):
    """
    Inicializa os grafos da matriz conectando seus vizinhos.

    Args:
        graph_matrix (list[list[Graph]]): Matriz de grafos.

    Returns:
        list[list[Graph]]: Matriz de grafos com adjacentes configurados.
    """
    rows = len(graph_matrix)
    columns = len(graph_matrix[0]) if rows > 0 else 0

    for l in range(rows):
        for c in range(columns):
            if isinstance(graph_matrix[l][c], Graph):
                # Verifica se é um grafo válido
                print(f"Graph ({l}, {c}): ", end="")

                # Baixo
                if l < rows - 1 and isinstance(graph_matrix[l + 1][c], Graph):
                    graph_matrix[l][c].add_adjacent(graph_matrix[l + 1][c])
                    print(f"({l + 1}, {c}) ", end="")

                # Cima
                if l > 0 and isinstance(graph_matrix[l - 1][c], Graph):
                    graph_matrix[l][c].add_adjacent(graph_matrix[l - 1][c])
                    print(f"({l - 1}, {c}) ", end="")

                # Direita
                if c < columns - 1 and isinstance(graph_matrix[l][c + 1], Graph):
                    graph_matrix[l][c].add_adjacent(graph_matrix[l][c + 1])
                    print(f"({l}, {c + 1}) ", end="")

                # Esquerda
                if c > 0 and isinstance(graph_matrix[l][c - 1], Graph):
                    graph_matrix[l][c].add_adjacent(graph_matrix[l][c - 1])
                    print(f"({l}, {c - 1}) ", end="")

                print("")  # Nova linha para cada grafo

    return graph_matrix


def initilize_game_matrix(game_matrix, terrains):
    """
    Inicializa a matriz do jogo com objetos Graph baseados no tipo de terreno.

    Args:
        game_matrix (list[list[int]]): Matriz de jogo com valores que indicam diferentes tipos de terreno.
        terrains (list[Terrain]): Lista de tipos de terreno.

    Returns:
        list[list[Graph]]: Matriz de grafos, onde cada célula é um objeto Graph, quando a célula não for uma parede.
    """
    game_rows = len(game_matrix)
    game_columns = len(game_matrix[0])

    for l in range(game_rows):
        for c in range(game_columns):
            if game_matrix[l][c] != 0:  # Ignora células de paredes
                if game_matrix[l][c] == 5:
                    game_matrix[l][c] = Graph(terrains[0], l, c, True)
                else:
                    game_matrix[l][c] = Graph(terrains[game_matrix[l][c] - 1], l, c)

    return game_matrix


def create_maze_surface(maze_pos_x, maze_pos_y, maze_square_size, graph_matrix, wall_color=(18, 9, 1)):
    """
    Cria a superfície visual do labirinto com base nos grafos e nas propriedades dos terrenos.

    Args:
        maze_pos_x (int): Posição x no eixo da tela onde o labirinto será desenhado.
        maze_pos_y (int): Posição y no eixo da tela onde o labirinto será desenhado.
        maze_square_size (int): Tamanho de cada célula do labirinto.
        graph_matrix (list[list[Graph]]): Matriz de grafos do labirinto.
        wall_color (tuple): Cor das paredes.

    Returns:
        pygame.Surface: Superfície com o labirinto renderizado.
    """
    rows = len(graph_matrix)
    columns = len(graph_matrix[0])

    # Cria uma superfície para o labirinto
    maze_surface = pygame.Surface((columns * maze_square_size, rows * maze_square_size), pygame.SRCALPHA)

    for l in range(rows):
        for c in range(columns):
            if graph_matrix[l][c] == 0:
                # Desenha as paredes
                pygame.draw.rect(maze_surface, wall_color,
                                 pygame.Rect(c * maze_square_size, l * maze_square_size, maze_square_size, maze_square_size))
            else:
                if graph_matrix[l][c].terrain_type.texture_image is None:
                    # Desenha o terreno sem textura
                    pygame.draw.rect(maze_surface, graph_matrix[l][c].terrain_type.rgb_color,
                                     pygame.Rect(c * maze_square_size, l * maze_square_size, maze_square_size, maze_square_size))
                else:
                    # Desenha o terreno com textura
                    maze_surface.blit(graph_matrix[l][c].terrain_type.texture_image,
                                      (c * maze_square_size, l * maze_square_size))
                if graph_matrix[l][c].reward:
                    # Desenha a recompensa, se houver
                    maze_surface.blit(reward_image, (c * maze_square_size, l * maze_square_size))

    return maze_surface


def load_matrix_from_file(file_path):
    """
    Lê uma matriz de um arquivo de texto.

    Args:
        file_path (str): Caminho para o arquivo.

    Returns:
        list[list[int]]: Matriz carregada como lista de listas de inteiros.
    """
    with open(file_path, 'r') as file:
        matrix = [
            list(map(int, line.split()))  # Converte cada linha em uma lista de inteiros
            for line in file
        ]
    return matrix


def get_click_position_in_matrix(click_pos, graph_matrix, maze_cords, maze_size, screen_size):
    """
    Determina a posição na matriz de grafos onde o mouse foi clicado.

    Args:
        click_pos (tuple): Posições x, y do clique.
        graph_matrix (list[list[Graph]]): Matriz de grafos.
        maze_cords (tuple): Coordenadas do labirinto na tela.
        maze_size (tuple): Tamanho do labirinto.
        screen_size (tuple): Tamanho da tela.

    Returns:
        dict: Um dicionário com a posição do clique e o tipo de célula (grafo ou parede), ou None se fora dos limites.
    """
    pos_x, pos_y = click_pos
    if pos_x < maze_cords[0] or pos_y < maze_cords[1] or pos_x >= maze_size[0] + maze_cords[0] or pos_y >= maze_size[1] + maze_cords[1]:
        print("Out of bounds")
        return None

    pos_x -= maze_cords[0]
    pos_y -= maze_cords[1]

    matrix_pos_x = pos_x // 15
    matrix_pos_y = pos_y // 15

    if isinstance(graph_matrix[matrix_pos_x][matrix_pos_y], Graph):
        return {'graph': [matrix_pos_x, matrix_pos_y]}
    else:
        return {'wall': [matrix_pos_x, matrix_pos_y]}


def draw_algorithm_path(screen, algorithm_path, maze_cords, maze_square_size, color):
    """
    Desenha o caminho percorrido pelo algoritmo.

    Args:
        screen (pygame.Surface): Superfície onde o caminho será desenhado.
        algorithm_path (list): Lista de coordenadas do caminho percorrido.
        maze_cords (tuple): Coordenadas do labirinto.
        maze_square_size (int): Tamanho de cada célula do labirinto.
        color (tuple): Cor usada para desenhar o caminho.
    """
    base_x, base_y = maze_cords

    square_surface = pygame.Surface((maze_square_size, maze_square_size), pygame.SRCALPHA)
    square_surface.fill((*color, 128))  # Cor com canal alpha

    for square_path in algorithm_path:
        pos_x = square_path[0][0] * maze_square_size + base_x
        pos_y = square_path[1][1] * maze_square_size + base_y

        # Desenha o quadrado semi-transparente na tela
        screen.blit(square_surface, (pos_x, pos_y))



def handle_mouse_click(event, graph_matrix, maze_x, maze_y, maze_width, maze_height, screen_size, positions):
    """
    Lida com o clique do mouse para definir as posições de início e fim no labirinto.

    Args:
        event (pygame.event): Evento de clique do mouse.
        graph_matrix (list[list[Graph]]): Matriz de grafos do labirinto.
        maze_x (int): Posição x do labirinto na tela.
        maze_y (int): Posição y do labirinto na tela.
        maze_width (int): Largura do labirinto.
        maze_height (int): Altura do labirinto.
        screen_size (tuple): Tamanho da tela.
        positions (dict): Dicionário com as posições de "início" e "fim".

    Returns:
        None
    """
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        x, y = event.pos
        graph_cord = get_click_position_in_matrix((x, y), graph_matrix, (maze_x, maze_y), (maze_width, maze_height), screen_size)
        if graph_cord is not None:
            if len(positions['starting']) == 0 and 'graph' in graph_cord:
                positions['starting'] = graph_cord['graph']
            elif len(positions['end']) == 0:
                positions['end'] = graph_cord[[key for key in graph_cord.keys()][0]]
            else:
                positions['starting'] = []
                positions['end'] = []
