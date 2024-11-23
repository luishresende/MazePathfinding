import cv2
import numpy as np


def print_unique_colors(image_path):
    """
    Lê uma imagem e imprime todos os valores únicos de cores RGB.

    Args:
        image_path (str): Caminho para a imagem.
    """
    # Carregar a imagem em formato RGB
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

    # Converter para formato RGB (OpenCV carrega em BGR por padrão)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Obter as cores únicas
    unique_colors = np.unique(image_rgb.reshape(-1, image_rgb.shape[2]), axis=0)

    # Imprimir as cores únicas
    print("Cores únicas na imagem (RGB):")
    for color in unique_colors:
        print(tuple(color))


def image_to_terrain_map_exact(image_path, map_size, terrain_colors):
    """
    Converte uma imagem RGB para uma matriz de terrenos (valores de 0 a 4)
    com base em cores exatas.

    Args:
        image_path (str): Caminho para a imagem de entrada.
        map_size (tuple): Tamanho da matriz resultante (linhas, colunas).
        terrain_colors (dict): Dicionário com cores RGB associadas aos terrenos.

    Returns:
        list: Matriz com valores representando o mapa de terrenos (0 a 4).
    """
    # Carregar a imagem em formato RGB
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

    # Redimensionar a imagem para o tamanho desejado
    resized_image = cv2.resize(image, (map_size[1], map_size[0]), interpolation=cv2.INTER_AREA)

    # Criar a matriz de terrenos
    terrain_map = []

    # Mapear os valores RGB para terrenos
    for row in resized_image:
        terrain_row = []
        for pixel in row:
            # Converter o pixel para uma tupla RGB
            pixel_rgb = tuple(pixel[::-1])  # OpenCV usa formato BGR, por isso invertemos

            # Verificar se o pixel corresponde a uma cor de terreno
            terrain = terrain_colors.get(pixel_rgb, 0)  # Padrão: 0 (parede)
            terrain_row.append(terrain)
        terrain_map.append(terrain_row)

    return terrain_map


# Definição das cores exatas para cada tipo de terreno
# Formato: {RGB: terreno}
terrain_colors = {
    (180, 180, 180): 1,  # Sólido e Plano (cinza claro)
    (70, 70, 70): 2,  # Rochoso (cinza escuro)
    (245, 228, 156): 3,  # Arenoso (marrom claro)
    (34, 177, 76): 4,      # Pântano (verde)
    (111, 49, 152): 5      # Terreno especial (roxo)
}

# Caminho para a imagem
image_path = "maze.png"

# Tamanho da matriz desejada (linhas, colunas)
map_size = (50, 50)

print_unique_colors(image_path)
# Gerar a matriz do mapa
terrain_map = image_to_terrain_map_exact(image_path, map_size, terrain_colors)

# Exibir a matriz
for row in terrain_map:
    for n in row:
        print(n, end=" ")
    print()