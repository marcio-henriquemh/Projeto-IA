from classe_ARESTAS import Aresta


class GuerraFria:

    # ---------------------------
    # VIZINHANÇA (N, S, L, O)
    # ---------------------------
    def adjacentes(self, i, j):
        possiveis = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
        return [(x,y) for x,y in possiveis if 0 <= x < 3 and 0 <= y < 3]


    # ---------------------------
    # VERIFICA VULNERABILIDADE
    # ---------------------------
    def vulneravel(self, tabuleiro, i, j, simbolo):

        inimigo = "U" if simbolo == "E" else "E"
        contador = 0

        for x, y in self.adjacentes(i, j):
            if tabuleiro[x][y] == inimigo:
                contador += 1

        return contador >= 2


    # ---------------------------
    # GERAR SUCESSORES
    # ---------------------------
    def gerar_sucessores(self, estado):

        sucessores = []
        simbolo = estado.simbolo()
        inimigo = "U" if simbolo == "E" else "E"

        for i in range(3):
            for j in range(3):

                # EXPANSÃO
                if estado.tabuleiro[i][j] == ".":
                    novo = estado.copiar()
                    novo.tabuleiro[i][j] = simbolo
                    novo.jogador = estado.trocar_jogador()

                    sucessores.append(
                        Aresta(novo, "expansao")
                    )

                # MUDANÇA DE REGIME
                elif estado.tabuleiro[i][j] == inimigo:
                    if self.vulneravel(estado.tabuleiro, i, j, inimigo):

                        novo = estado.copiar()
                        novo.tabuleiro[i][j] = simbolo
                        novo.jogador = estado.trocar_jogador()

                        sucessores.append(
                            Aresta(novo, "mudanca_regime")
                        )

        return sucessores


    # ---------------------------
    # FUNÇÃO HEURÍSTICA
    # ---------------------------
    def avaliar(self, estado):

        score = 0

        for i in range(3):
            for j in range(3):

                if estado.tabuleiro[i][j] == "E":
                    score += 1

                    # centralidade estratégica
                    if (i, j) == (1, 1):
                        score += 0.5

                    # vulnerabilidade
                    if self.vulneravel(estado.tabuleiro, i, j, "E"):
                        score -= 2

                elif estado.tabuleiro[i][j] == "U":
                    score -= 1

                    if (i, j) == (1, 1):
                        score -= 0.5

                    if self.vulneravel(estado.tabuleiro, i, j, "U"):
                        score += 2

        return score


    # ---------------------------
    # ESTADO TERMINAL
    # ---------------------------
    def terminal(self, estado):
        return all("." not in linha for linha in estado.tabuleiro)