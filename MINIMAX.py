
'''
Docstring para MINIMAX
'''

class Estrutura_PAIS:

    """
    Representa um país no grafo de relações.

    Atributos:
        nome_pais (str): O nome do país.
    """
    def __init__(self, nome_pais):
        self.nome_pais=nome_pais

class Estrutura_RELACAO:

    '''''
    Representa uma relação entre dois países (aresta no grafo).

    Atributos:
        pais1 (str/Estrutura_PAIS): O primeiro país da relação.
        pais2 (str/Estrutura_PAIS): O segundo país da relação.
        sinal_peso (int): O peso/sinal da relação (ex: +1 para aliado, -1 para inimigo)
    '''


    def __init__(self,pais1,pais2,sinal_peso):
        self.pais1=pais1
        self.pais2=pais2
        self.sinal_peso=sinal_peso



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
    

    '''

    Regras do conflito 

    AlianÇA entre ALIADOS- +
    CONFLITO ENTRE ALIADOS X EIXO=+
    ALIANCA ALIADO X EIXO=-
    ALIANCA ENTRE EIXO =-
    '''