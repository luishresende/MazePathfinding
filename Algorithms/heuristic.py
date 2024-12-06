import math
from Game import *


# Heurística combinada
def heuristic(current_node, target_pos, reward_value=10, weights=(1, 1, 1)):
    """
    Calcula a heurística combinada para o nó atual.

    current: tuple (x, y) - Posição atual do agente.
    goal: tuple (x, y) - Posição do objetivo final.
    grid: 2D list - Representação do terreno, onde os valores são os tipos de terreno.
    rewards: list of tuples - Lista de posições onde há recompensas no mapa.
    reward_value: int - Valor padrão de uma recompensa.
    weights: tuple - Pesos (w1, w2, w3) para distância, custo do terreno e recompensa, respectivamente.
    """

    rewards = [(1, 22), (3, 7), (4, 16), (7, 42), (11, 21), (11, 32), (15, 5),
               (15, 21), (15, 32), (15, 41), (23, 17), (23, 23), (23, 30), (23, 34),
               (23, 40), (27, 25), (27, 28), (28, 17), (28, 40), (30, 11), (30, 21),
               (30, 32), (30, 36), (32, 21), (36, 28), (39, 33), (39, 35), (39, 37),
               (40, 16), (41, 33), (41, 35), (41, 37), (42, 40), (43, 33), (43, 35),
               (43, 37), (45, 12)]

    w1, w2, w3 = weights

    # Distância Manhattan para o objetivo
    current_pos = (current_node.matrix_position_x, current_node.matrix_position_y)
    distance = abs(target_pos[0] - current_pos[0]) + abs(target_pos[1] - current_pos[1])

    # Custo do terreno no nó atual
    terrain_type = terrains.index(current_node.terrain_type)
    terrain_cost = terrains[terrain_type].default_coast  # Custo infinito se for parede

    # Atração por recompensas próximas
    reward_influence = 0
    for reward in rewards:
        reward_distance = abs(reward[0] - current_pos[0]) + abs(reward[1] - current_pos[1])
        if reward_distance <= 1:  # Considera apenas recompensas próximas
            reward_influence -= reward_value / (reward_distance + 1)

    # Combina os fatores na heurística
    return w1 * distance + w2 * terrain_cost + w3 * reward_influence