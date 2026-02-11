class Aresta:
    def __init__(self, estado_destino, tipo, peso, sinal):
        self.estado_destino = estado_destino
        self.tipo = tipo
        self.peso = peso
        self.sinal = sinal

    def valor(self):
        return self.peso * self.sinal
