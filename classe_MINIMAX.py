class Minimax:
    def __init__(self, jogo, profundidade=3):
        self.jogo = jogo
        self.profundidade = profundidade

    # ---------------------------
    # FUNÇÃO RECURSIVA ALFA-BETA
    # ---------------------------
    def executar(self, estado, profundidade, alpha, beta, maximizando):

        if profundidade == 0 or self.jogo.terminal(estado):
            return self.jogo.avaliar(estado)

        sucessores = self.jogo.gerar_sucessores(estado)

        if not sucessores:
            return self.jogo.avaliar(estado)

        if maximizando:

            valor = float("-inf")

            for aresta in sucessores:

                valor = max(
                    valor,
                    self.executar(
                        aresta.estado_destino,
                        profundidade - 1,
                        alpha,
                        beta,
                        False
                    )
                )

                alpha = max(alpha, valor)

                # PODA
                if alpha >= beta:
                    break

            return valor

        else:

            valor = float("inf")

            for aresta in sucessores:

                valor = min(
                    valor,
                    self.executar(
                        aresta.estado_destino,
                        profundidade - 1,
                        alpha,
                        beta,
                        True
                    )
                )

                beta = min(beta, valor)

                # PODA
                if beta <= alpha:
                    break

            return valor


    # ---------------------------
    # ESCOLHE MELHOR JOGADA
    # ---------------------------
    def melhor_jogada(self, estado):

        melhor_valor = float("-inf")
        melhor_aresta = None

        alpha = float("-inf")
        beta = float("inf")

        for aresta in self.jogo.gerar_sucessores(estado):

            valor = self.executar(
                aresta.estado_destino,
                self.profundidade - 1,
                alpha,
                beta,
                False
            )

            if valor > melhor_valor:
                melhor_valor = valor
                melhor_aresta = aresta

            alpha = max(alpha, melhor_valor)

        return melhor_aresta