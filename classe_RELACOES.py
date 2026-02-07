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