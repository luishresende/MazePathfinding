from Game.Graph import Graph
from .TerrainType import TerrainType
from .Graph import Graph
from .AlgorithmPathManager import AlgorithmPathManager

import pygame

positions = {
    'starting': [],
    'end': []
}
reward_image = pygame.image.load('textures/bolsa-de-dinheiro2.png')
solo_arenoso = pygame.image.load('textures/arenoso_textura.png')
solo_pantano = pygame.image.load('textures/pantano_textura.png')
solo_rochoso = pygame.image.load('textures/rochoso_textura.png')
solo_plano = pygame.image.load('textures/plano_textura.png')
finish_line = pygame.image.load('textures/finish.png')
player = pygame.image.load('textures/smile.png')
play_button = {'textures': [pygame.image.load('textures/play_button.png'), pygame.image.load('textures/on_play_button.png')],
               'position': (835, 838),
               'size': (49, 49),
               'clicked': False,
               'blocked': True}
reset_button = {'textures': [pygame.image.load('textures/reset_button.png'), pygame.image.load('textures/on_reset_button.png')],
               'position': (770, 838),
               'size': (49, 49),
               'clicked': False}



solid_and_flat = TerrainType("Sólido e Plano", 1, (194, 192, 192), solo_plano)
rocky = TerrainType("Rochoso", 10, (128, 128, 128), solo_rochoso)
sandy = TerrainType("Arenoso", 4, (245, 228, 156), solo_arenoso)
swamp = TerrainType("Pântano", 20, (34, 177, 76), solo_pantano)
terrains = [solid_and_flat, rocky, sandy, swamp]
algorith_path_manager = AlgorithmPathManager()

screen_size = (900, 900)
# Definindo a posição e tamanho do labirinto na tela
maze_width = screen_size[1] - 150
maze_height = screen_size[0] - 150
maze_x = 75
maze_y = 75
surface_manager = None