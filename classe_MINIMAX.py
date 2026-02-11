class Minimax:
    def __init__(self, jogo, profundidade=3):
        self.jogo = jogo
        self.profundidade = profundidade

    def executar(self, estado, profundidade, maximizando):
        if profundidade == 0 or self.jogo.terminal(estado):
            return self.jogo.avaliar(estado)

        sucessores = self.jogo.gerar_sucessores(estado)

        if maximizando:
            melhor = float("-inf")
            for aresta in sucessores:
                valor = aresta.valor() + self.executar(aresta.estado_destino, profundidade-1, False)
                melhor = max(melhor, valor)
            return melhor
        else:
            pior = float("inf")
            for aresta in sucessores:
                valor = aresta.valor() + self.executar(aresta.estado_destino, profundidade-1, True)
                pior = min(pior, valor)
            return pior

    def melhor_jogada(self, estado):
        melhor_valor = float("-inf")
        melhor_aresta = None

        for aresta in self.jogo.gerar_sucessores(estado):
            valor = self.executar(aresta.estado_destino, self.profundidade, False)
            if valor > melhor_valor:
                melhor_valor = valor
                melhor_aresta = aresta

        return melhor_aresta
