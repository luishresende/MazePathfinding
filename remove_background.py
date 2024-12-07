import cv2
import numpy as np
import os


def remove_black_background(input_dir, output_dir):
    """
    Remove fundos pretos de imagens, mantendo apenas os pixels brancos,
    e salva imagens com fundo transparente, preservando o tamanho original.

    :param input_dir: Diretório contendo as imagens de entrada.
    :param output_dir: Diretório onde as imagens processadas serão salvas.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Caminho completo para o arquivo
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.png')

            # Carregar a imagem no modo original (mantendo dimensões)
            image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
            if image is None:
                print(f"Não foi possível carregar {filename}, pulando...")
                continue

            # Converter para escala de cinza para criar a máscara
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Criar uma máscara binária para pixels brancos
            _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

            # Criar uma nova imagem com canal alpha
            result = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
            result[:, :, 3] = mask  # Define o canal alpha com base na máscara

            # Salvar a imagem com fundo transparente
            cv2.imwrite(output_path, result)
            print(f"Imagem processada: {filename}")


# Configuração de diretórios
input_directory = "/home/luis/Downloads/bfs/"
output_directory = "/home/luis/PycharmProjects/Labirinto/textures/algorithms/"

# Processar as imagens
remove_black_background(input_directory, output_directory)
