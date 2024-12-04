from Algorithms.bfs import bfs
from Algorithms.dfs import dfs
from Algorithms.greedy_search import greedy_search
from Algorithms.search_star import search_star
from Game import *
from Game.GameFunctions import *
from Game.AlgorithmPathManager import AlgorithmPathManager
from Game.SurfaceManager import SurfaceManager

import pygame
import threading

clock = pygame.time.Clock()

# Carrega a matriz do labirinto e inicializa os grafos
game_matrix = load_matrix_from_file('maze.txt')
print(game_matrix)
graph_matrix = initilize_game_matrix(game_matrix, terrains)
graph_matrix = initialize_graphs(graph_matrix)
pygame.init()

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Labirinto Inteligente")

# Criação da superfície do labirinto
maze_surface = create_maze_surface(maze_x, maze_y, 15, graph_matrix)

surface_manager = SurfaceManager(maze_surface)

# Definindo as variáveis de controle
positions = {'starting': [], 'end': []}  # Posições do início e fim
algorith_path_manager = AlgorithmPathManager  # Caminho do algoritmo (ainda não implementado)
running = True
running_algorithm = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Lida com o clique do mouse para definir as posições de início e fim
        handle_mouse_click(event, graph_matrix, maze_x, maze_y, maze_width, maze_height, screen_size, positions)

    # Preenchendo o fundo
    screen.fill((64, 80, 67))  # Cor do fundo

    # Desenhando o contorno do labirinto
    pygame.draw.rect(screen, (36, 1, 10), pygame.Rect(maze_x, maze_y, maze_width, maze_height))

    # Exibindo o labirinto na tela
    screen.blit(surface_manager.get_surface(), (maze_x, maze_y))

    # Exibindo o jogador (se a posição inicial estiver definida)
    if len(positions['starting']) != 0:
        screen.blit(player, (positions['starting'][0] * 15 + maze_x, positions['starting'][1] * 15 + maze_y))

    # Exibindo a linha de chegada (se a posição final estiver definida)
    if len(positions['end']) != 0:
        screen.blit(finish_line, (positions['end'][0] * 15 + maze_x, positions['end'][1] * 15 + maze_y))

    # Se o início e fim estiverem definidos, chama o algoritmo de busca para encontrar o caminho
    if not running_algorithm and len(positions['starting']) != 0 and len(positions['end']) != 0:
        # Chama o algoritmo de busca (Exemplo: A* ou BFS)
        # O algoritmo deve retornar o caminho, e o caminho será exibido

        end_pos = tuple(positions['end'])
        # Algoritmo de busca (A ser implementado)
        # Exemplo fictício, substitua com seu algoritmo real:
        print(graph_matrix[positions['starting'][0]][positions['starting'][1]].matrix_position_y, graph_matrix[positions['starting'][0]][positions['starting'][1]].matrix_position_x)
        thread = threading.Thread(target=search_star, args=(graph_matrix[positions['starting'][1]][positions['starting'][0]], end_pos, surface_manager, game_matrix))
        thread.start()
        running_algorithm = True


    '''# Desenhando o caminho encontrado (se houver)
    if len(algorith_path) > 0:
        draw_algorithm_path(screen, algorith_path, (maze_x, maze_y), 15, (255, 0, 0))'''

    # Atualizando a tela
    pygame.display.flip()
    clock.tick(60)  # Controla a taxa de atualização do jogo

# Finalizando o Pygame
pygame.quit()
