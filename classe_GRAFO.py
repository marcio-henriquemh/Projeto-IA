class Estrutura_GRAFO:

    '''
    Docstring para Estrutura_GRAFO

    """
    Representa o grafo completo das relações entre países para o algoritmo Minimax.

    Atributos:
        lista_relacoes (list[Estrutura_RELACAO]): Lista de objetos de relação (arestas).
    """
    '''
    def __init__(self, Lista_relacoes):
        self.lista_relacoes=Lista_relacoes


    def exibir_grafo(self):
        print("Estrutura do Grafo (Relações):")
        for rel in self.lista_relacoes:
            print(f"  {rel}")
    

    '''

    Regras do conflito 

    AlianÇA entre ALIADOS- +
    CONFLITO ENTRE ALIADOS X EIXO=+
    ALIANCA ALIADO X EIXO=-
    ALIANCA ENTRE EIXO =-
    '''