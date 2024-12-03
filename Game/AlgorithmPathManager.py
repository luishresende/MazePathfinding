from threading import Lock

class AlgorithmPathManager:
    def __init__(self):
        self.algorithm_path = []
        self.lock = Lock()

    def update_algorithm_path(self, new_path):
        """
        Atualiza o caminho do algoritmo de forma segura com um bloqueio.

        Args:
            new_path (list): O novo caminho a ser adicionado.
        """
        with self.lock:  # Garante acesso exclusivo à variável
            self.algorithm_path.extend(new_path)

    def get_algorithm_path(self):
        """
        Retorna o caminho do algoritmo de forma segura.

        Returns:
            list: Uma cópia do caminho atual.
        """
        with self.lock:  # Garante acesso exclusivo à variável
            return list(self.algorithm_path)  # Retorna uma cópia para evitar modificações externas

    def add_path(self, graph):
        """
        Retorna o caminho do algoritmo de forma segura.

        Returns:
            list: Uma cópia do caminho atual.
        """
        with self.lock:  # Garante acesso exclusivo à variável
            self.algorithm_path.append(graph)  # Retorna uma cópia para evitar modificações externas
            return list(self.algorithm_path)