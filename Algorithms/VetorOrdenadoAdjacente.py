import heapq

class VetorOrdenadoAdjacente:
    def __init__(self):
        self.heap = []  # Usamos um heap para manter os elementos ordenados.
        self.counter = 0  # Para desempate em casos de valores iguais.

    def inserir(self, adjacente, custo_g, heuristica, caminho):
        # Calcula o custo total (f = g + h)
        custo_total = custo_g + heuristica
        # Adiciona o adjacente ao heap, com um contador para evitar problemas de ordenação de objetos.
        heapq.heappush(self.heap, (custo_total, self.counter, adjacente, custo_g, caminho))
        self.counter += 1

    def get_primeiro(self):
        # Remove e retorna o elemento de menor custo (f)
        if self.heap:
            return heapq.heappop(self.heap)
        return None

    def is_empty(self):
        # Verifica se o heap está vazio
        return len(self.heap) == 0
