class Minimax:
    def __init__(self, jogo, profundidade=3):
        self.jogo = jogo
        self.profundidade = profundidade

    # FUNÇÃO RECURSIVA ALFA-BETA- tem como intuição explorar o espaço de estados de forma eficiente, evitando 
    # a avaliação de ramos que não influenciarão a decisão final, e assim, otimizando o processo de tomada de decisão do agente.
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

                # PODA- Se o valor atual é maior ou igual ao beta, não precisamos explorar mais esse ramo,
                #  pois o oponente escolheria uma jogada que minimizaria nosso ganho.

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


    # ESCOLHE MELHOR JOGADA- O método melhor_jogada é responsável 
    # por iterar sobre os sucessores do estado atual, utilizando a função executar para avaliar cada um deles, e selecionando aquele que oferece o maior valor de avaliação, ou seja, a melhor jogada para o agente. Ele também implementa a lógica de atualização dos valores alpha e beta para otimizar a busca, garantindo que o agente tome decisões informadas
    #  e estratégicas com base na análise do espaço de estados.
    def melhor_jogada(self, estado):
        # Verifica quem está jogando para decidir se maximiza ou minimiza
        maximizando = (estado.jogador == "EUA")
        
        melhor_valor = float("-inf") if maximizando else float("inf")
        melhor_aresta = None

        alpha = float("-inf")
        beta = float("inf")

        for aresta in self.jogo.gerar_sucessores(estado):
            # Se EUA jogou, o próximo nível (executar) é a vez da URSS (False)
            # Se URSS jogou, o próximo nível é a vez dos EUA (True)
            proximo_maximizando = not maximizando
            
            valor = self.executar(
                aresta.estado_destino,
                self.profundidade - 1,
                alpha,
                beta,
                proximo_maximizando
            )

            if maximizando:
                if valor > melhor_valor:
                    melhor_valor = valor
                    melhor_aresta = aresta
                alpha = max(alpha, melhor_valor)
            else:
                if valor < melhor_valor:
                    melhor_valor = valor
                    melhor_aresta = aresta
                beta = min(beta, melhor_valor)

        return melhor_aresta