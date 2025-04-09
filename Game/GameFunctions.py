from copy import deepcopy
from time import sleep

from Game.Graph import Graph
from Game import reward_image, play_button, maze_x, maze_y, algorithm_sleep_time
import Game

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
            # Verifica se é um grafo válido
            if isinstance(graph_matrix[l][c], Graph):

                # Baixo
                if l < rows - 1 and isinstance(graph_matrix[l + 1][c], Graph):
                    graph_matrix[l][c].add_adjacent(graph_matrix[l + 1][c])

                # Cima
                if l > 0 and isinstance(graph_matrix[l - 1][c], Graph):
                    graph_matrix[l][c].add_adjacent(graph_matrix[l - 1][c])

                # Direita
                if c < columns - 1 and isinstance(graph_matrix[l][c + 1], Graph):
                    graph_matrix[l][c].add_adjacent(graph_matrix[l][c + 1])

                # Esquerda
                if c > 0 and isinstance(graph_matrix[l][c - 1], Graph):
                    graph_matrix[l][c].add_adjacent(graph_matrix[l][c - 1])

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
    graph_matrix = deepcopy(game_matrix)

    for l in range(game_rows):
        for c in range(game_columns):
            if graph_matrix[l][c] != 0:  # Ignora células de paredes
                if graph_matrix[l][c] == 5:
                    graph_matrix[l][c] = Graph(terrains[0], c, l, True)
                else:
                    terrain_type = graph_matrix[l][c]
                    graph_matrix[l][c] = Graph(terrains[terrain_type - 1], c, l)

    return graph_matrix


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


def click_in_matrix(click_pos, maze_cords, maze_size):
    pos_x, pos_y = click_pos
    return not (pos_x < maze_cords[0] or pos_y < maze_cords[1] or pos_x >= maze_size[0] + maze_cords[0] or pos_y >= maze_size[1] + maze_cords[1])


def click_in_button(click_pos, button):
    x, y = click_pos
    btn_pos_x, btn_pos_y = button['position']
    btn_width, btn_height = button['size']
    return btn_pos_x < x < btn_pos_x + btn_width and btn_pos_y < y < btn_pos_y + btn_height


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

    pos_x -= maze_cords[0]
    pos_y -= maze_cords[1]

    matrix_pos_x = pos_x // 15
    matrix_pos_y = pos_y // 15

    if isinstance(graph_matrix[matrix_pos_y][matrix_pos_x], Graph):
        return {'graph': [matrix_pos_x, matrix_pos_y]}
    else:
        return {'wall': [matrix_pos_x, matrix_pos_y]}


'''def draw_algorithm_path(color):
    """
    Desenha o caminho percorrido pelo algoritmo.

    Args:
        color (tuple): Cor usada para desenhar o caminho.
    """

    square_surface.fill((*color, 128))  # Cor com canal alpha

    for graph in algorith_path_manager.get_algorithm_path():
        pos_x = graph.matrix_position_x * maze_square_size + maze_x
        pos_y = graph.matrix_position_y * maze_square_size + maze_y

        # Desenha o quadrado semi-transparente na tela
        screen.blit(square_surface, (pos_x, pos_y))'''



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
        positions_defined = len(positions['starting'] + positions['end']) == 4
        if not positions_defined and click_in_matrix((x, y), (maze_x, maze_y), (maze_width, maze_height)):
            graph_cord = get_click_position_in_matrix((x, y), graph_matrix, (maze_x, maze_y), (maze_width, maze_height), screen_size)
            if graph_cord is not None:
                if len(positions['starting']) == 0:
                    if 'graph' in graph_cord:
                        positions['starting'] = graph_cord['graph']
                elif not Game.waiting_restart and len(positions['end']) == 0:
                    positions['end'] = graph_cord[[key for key in graph_cord.keys()][0]]
                    if Game.selected_algorithm != 0:
                        Game.play_button['blocked'] = False
        elif not play_button['blocked'] and positions_defined and click_in_button((x, y), Game.play_button):
                Game.play_button['clicked'] = True
        elif click_in_button((x, y), Game.reset_button):
            positions['starting'] = positions['end'] = []
            Game.play_button['blocked'] = True
            Game.surface_manager.reset_surface()
            Game.waiting_restart = False
        elif click_in_button((x, y), Game.previous_button):
            if Game.selected_algorithm == 1:
                Game.selected_algorithm = 4
            else:
                Game.selected_algorithm -= 1
            if len(positions['starting'] + positions['end']) == 4:
                Game.play_button['blocked'] = False
        elif click_in_button((x, y), Game.next_button):
            if Game.selected_algorithm == 4:
                Game.selected_algorithm = 1
            else:
                Game.selected_algorithm += 1
            if len(positions['starting'] + positions['end']) == 4:
                Game.play_button['blocked'] = False



def update_maze_surface_algorithm(surface, graph, color, maze_square_size):
    """
    Atualiza a superfície com base no nó do grafo.

    Args:
        surface (pygame.Surface): A superfície onde será desenhado.
        graph (Graph): O nó do grafo percorrido.
        color (tuple): Cor usada para desenhar o caminho.
        maze_square_size (int): Tamanho de cada célula do labirinto.
        maze_x (int): Posição x inicial do labirinto na tela.
        maze_y (int): Posição y inicial do labirinto na tela.
    """
    # Cria a superfície para desenhar os quadrados semi-transparentes
    square_surface = pygame.Surface((maze_square_size, maze_square_size), pygame.SRCALPHA)
    square_surface.fill((*color, 128))  # Cor com canal alpha

    # Calcula a posição do quadrado
    pos_x = graph.matrix_position_x * maze_square_size
    pos_y = graph.matrix_position_y * maze_square_size

    # Atualiza a superfície fornecida
    surface.blit(square_surface, (pos_x, pos_y))


def update_player_road(path):
    for graph in path:
        sleep(0.1)
        Game.positions['starting'] = [graph.matrix_position_x, graph.matrix_position_y]

    Game.positions['end'] = []


def draw_player(screen, player_sprite, matrix_position):
    pos_x, pos_y = matrix_position[0] * 15 + maze_x, matrix_position[1] * 15 + maze_y
    screen.blit(player_sprite, (pos_x, pos_y))


def format_time(timestamp):
    """
    Formata um timestamp em horas:minutos:segundos:milissegundos.

    Args:
        timestamp (float): O tempo em segundos como retorno de time.time().

    Returns:
        str: O tempo formatado em "HH:MM:SS:MMM".
    """
    # Divide o timestamp em segundos inteiros e milissegundos
    seconds = int(timestamp)
    milliseconds = int((timestamp - seconds) * 1000)

    # Converte os segundos para horas, minutos e segundos
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    # Formata o tempo como string
    return f"{hours:02}:{minutes:02}:{seconds:02}:{milliseconds:03}"