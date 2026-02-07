import copy

'''
    Regras do conflito 
    AlianÇA entre ALIADOS- +
    CONFLITO ENTRE ALIADOS X EIXO=+
    ALIANCA ALIADO X EIXO=-
    ALIANCA ENTRE EIXO =-
'''

class Estrutura_GRAFO:
    '''
    Docstring para Estrutura_GRAFO
   
    Representa o grafo completo das relações entre países para o algoritmo Minimax.

    Atributos:
        lista_relacoes (list[Estrutura_RELACAO]): Lista de objetos de relação (arestas).
    '''
    
    def __init__(self, lista_relacoes, blocos=None):  # blocos é opcional
        self.lista_relacoes = lista_relacoes
        
        if blocos is None:
            # Blocos padrão
            self.blocos = {
                "Eixo": ["Alemanha", "Japão", "Itália"],
                "Aliados": ["Reino Unido", "EUA", "União Soviética", "França"]
            }
        else:
            self.blocos = blocos
    
    def copiar(self):
        """Cria uma cópia profunda do grafo"""
        return Estrutura_GRAFO(
            copy.deepcopy(self.lista_relacoes),
            copy.deepcopy(self.blocos)
        )

    def auxiliar_blocos(self, pais1, pais2):
        # Se são objetos PAIS, pega o nome
        if hasattr(pais1, 'nome_pais'):
            nome1 = pais1.nome_pais
            nome2 = pais2.nome_pais
        else:
            nome1 = pais1
            nome2 = pais2
            
        # Verifica se ambos estão nos Aliados
        if nome1 in self.blocos["Aliados"] and nome2 in self.blocos["Aliados"]:
            return True
        # Verifica se ambos estão no Eixo
        elif nome1 in self.blocos["Eixo"] and nome2 in self.blocos["Eixo"]:
            return True
        # Caso contrário
        else:
            return False
    
    def exibir_grafo(self):
        print("Estrutura do Grafo (Relações):")
        for i, rel in enumerate(self.lista_relacoes):
            print(f"  [{i}] {rel}")
    
    def get_relacao(self, index):
        """Retorna uma relação pelo índice"""
        if 0 <= index < len(self.lista_relacoes):
            return self.lista_relacoes[index]
        return None