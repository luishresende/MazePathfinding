from Algorithms import bfs, dfs, greedy_search, search_star
from Game import terrains, screen_size, maze_x, maze_y, maze_width, maze_height, player, finish_line, previous_button, next_button, label, selected_algorithm
import Game
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

Game.surface_manager = SurfaceManager(maze_surface)
Game.algorithms = {
    'default':{
        'function': None,
        'label': pygame.image.load('textures/algorithms/default.png')
    },
    'star': {
        'function': search_star.search_star,
        'label': pygame.image.load('textures/algorithms/star.png')
    },
    'bfs': {
        'function': bfs.bfs,
        'label': pygame.image.load('textures/algorithms/bfs.png')
    },
    'dfs': {
        'function': dfs.dfs,
        'label': pygame.image.load('textures/algorithms/dfs.png')
    },
    'greedy': {
        'function': greedy_search.greedy_search,
        'label': pygame.image.load('textures/algorithms/greedy.png')
    }
}
algorithms_names = [key for key in Game.algorithms.keys()]


# Definindo as variáveis de controle
positions = {'starting': [], 'end': []}  # Posições do início e fim
algorith_path_manager = AlgorithmPathManager  # Caminho do algoritmo (ainda não implementado)
running = True


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
    screen.blit(Game.surface_manager.get_surface(), (maze_x, maze_y))

    # Exibindo o jogador (se a posição inicial estiver definida)
    if len(positions['starting']) != 0:
        screen.blit(player, (positions['starting'][0] * 15 + maze_x, positions['starting'][1] * 15 + maze_y))

    # Exibindo a linha de chegada (se a posição final estiver definida)
    if len(positions['end']) != 0:
        screen.blit(finish_line, (positions['end'][0] * 15 + maze_x, positions['end'][1] * 15 + maze_y))

    # Se o início e fim estiverem definidos, chama o algoritmo de busca para encontrar o caminho
    if Game.play_button['clicked'] and not Game.play_button['blocked']:
        end_pos = tuple(positions['end'])

        def thread_target():
            # Executa o algoritmo de busca
            Game.algorithms[algorithms_names[Game.selected_algorithm]]['function'](
                graph_matrix[positions['starting'][1]][positions['starting'][0]],
                end_pos,
                Game.surface_manager,
                game_matrix
            )
            # Após a execução do algoritmo, desbloqueia o botão
            Game.play_button['blocked'] = False

        # Cria e inicia a thread
        thread = threading.Thread(target=thread_target)
        thread.start()

        Game.play_button['clicked'] = False
        Game.play_button['blocked'] = True

    mouse_pos = pygame.mouse.get_pos()
    if not Game.play_button['blocked'] and click_in_button(mouse_pos, Game.play_button):
        screen.blit(Game.play_button['textures'][1], Game.play_button['position'])
    else:
        screen.blit(Game.play_button['textures'][0], Game.play_button['position'])

    if click_in_button(mouse_pos, Game.reset_button):
        screen.blit(Game.reset_button['textures'][1], Game.reset_button['position'])
    else:
        screen.blit(Game.reset_button['textures'][0], Game.reset_button['position'])

    if not previous_button['clicked'] and click_in_button(mouse_pos, previous_button):
        screen.blit(previous_button['textures'][1], previous_button['position'])
    else:
        screen.blit(previous_button['textures'][0], previous_button['position'])

    if not next_button['clicked'] and click_in_button(mouse_pos, next_button):
        screen.blit(next_button['textures'][1], next_button['position'])
    else:
        screen.blit(next_button['textures'][0], next_button['position'])

    screen.blit(label, (285, 13))
    screen.blit(Game.algorithms[algorithms_names[Game.selected_algorithm]]['label'], (285, 13))



    '''# Desenhando o caminho encontrado (se houver)
    if len(algorith_path) > 0:
        draw_algorithm_path(screen, algorith_path, (maze_x, maze_y), 15, (255, 0, 0))'''

    # Atualizando a tela
    pygame.display.flip()
    clock.tick(60)  # Controla a taxa de atualização do jogo

# Finalizando o Pygame
pygame.quit()
