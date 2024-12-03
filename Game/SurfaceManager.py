from threading import Lock

class SurfaceManager:
    def __init__(self, surface):
        """
        Inicializa o gerenciador de superfície com uma superfície existente.

        Args:
            surface (pygame.Surface): A superfície a ser gerenciada.
        """
        self.lock = Lock()
        self.surface = surface

    def update_surface(self, draw_function, *args, **kwargs):
        """
        Atualiza a superfície de forma segura chamando uma função de desenho.

        Args:
            draw_function (callable): Função que desenha na superfície.
            *args: Argumentos posicionais para a função de desenho.
            **kwargs: Argumentos nomeados para a função de desenho.
        """
        with self.lock:
            draw_function(self.surface, *args, **kwargs)

    def get_surface(self):
        """
        Retorna uma cópia da superfície de forma segura.

        Returns:
            pygame.Surface: Cópia da superfície atual.
        """
        with self.lock:
            return self.surface.copy()  # Retorna uma cópia para evitar modificações externas
