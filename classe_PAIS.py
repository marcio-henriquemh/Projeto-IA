

class Estrutura_PAIS:
    """
    Representa um país no grafo de relações.

    Atributos:
        nome_pais (str): O nome do país.
    """
    def __init__(self, nome_pais):
        self.nome_pais = nome_pais
    
    def __str__(self):
        return self.nome_pais
    
    def __repr__(self):
        return f"PAIS({self.nome_pais})"
