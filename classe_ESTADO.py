import copy
from classe_GRAFO import Estrutura_GRAFO

class EstadoJogo:
    """Representa um estado do jogo com todas as informações necessárias"""
    
    def __init__(self, grafo, jogador_atual="ALIADOS", profundidade=0):
        self.grafo = grafo
        self.jogador_atual = jogador_atual  # "ALIADOS" ou "EIXO"
        self.profundidade = profundidade
    
    def copiar(self):
        """Cria uma cópia profunda do estado"""
        return EstadoJogo(
            copy.deepcopy(self.grafo),
            self.jogador_atual,
            self.profundidade
        )
    
    def __str__(self):
        return f"Estado(prof={self.profundidade}, jogador={self.jogador_atual})"
    
    def __repr__(self):
        return self.__str__()