class Estrutura_RELACAO:
    '''Representa uma relação entre dois países (aresta no grafo).

    Atributos:
        pais1 (str/Estrutura_PAIS): O primeiro país da relação.
        pais2 (str/Estrutura_PAIS): O segundo país da relação.
        sinal_peso (int): O peso/sinal da relação (ex: +1 para aliado, -1 para inimigo)
    '''

    def __init__(self, pais1, pais2, sinal_peso):
        self.pais1 = pais1
        self.pais2 = pais2
        self.sinal_peso = sinal_peso
    
    def __str__(self):
        # Se são objetos PAIS, pega o nome
        if hasattr(self.pais1, 'nome_pais'):
            nome1 = self.pais1.nome_pais
            nome2 = self.pais2.nome_pais
        else:
            nome1 = self.pais1
            nome2 = self.pais2
        
        sinal = "+" if self.sinal_peso >= 0 else ""
        return f"({nome1}, {nome2}, {sinal}{self.sinal_peso})"
    
    def __repr__(self):
        return self.__str__()
    
    def copiar(self):
        """Cria uma cópia da relação"""
        import copy
        return Estrutura_RELACAO(
            copy.deepcopy(self.pais1),
            copy.deepcopy(self.pais2),
            self.sinal_peso
        )