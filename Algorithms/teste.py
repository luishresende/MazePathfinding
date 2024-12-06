# Função para ler o arquivo e processar a matriz
def extrair_posicoes_arquivo(caminho_arquivo):
    posicoes = []

    # Lê o arquivo e converte em uma lista de listas
    with open(caminho_arquivo, 'r') as file:
        matriz = [list(map(int, linha.split())) for linha in file.readlines()]

    # Itera pela matriz para encontrar as posições com valor 5
    for i, linha in enumerate(matriz):
        for j, valor in enumerate(linha):
            if valor == 5:
                posicoes.append((i, j))  # Armazena a posição (linha, coluna)

    return posicoes


# Caminho do arquivo TXT (modifique o caminho conforme necessário)
caminho_arquivo = '../maze.txt'

# Chama a função e imprime as posições
posicoes = extrair_posicoes_arquivo(caminho_arquivo)
print("Posições com valor 5:", posicoes)
