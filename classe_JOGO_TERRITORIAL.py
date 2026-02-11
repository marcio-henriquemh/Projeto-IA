from classe_ARESTAS import Aresta


class GuerraFria:

    def adjacentes(self, i, j):
        possiveis = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
        return [(x,y) for x,y in possiveis if 0 <= x < 3 and 0 <= y < 3]
    
    def pode_mudar_regime(self, tabuleiro, i, j, jogador):
        inimigo = "U" if jogador == "EUA" else "E"
        contador = 0

        for x,y in self.adjacentes(i,j):
            if tabuleiro[x][y] == inimigo:
                contador += 1

        return contador >= 2
    
    def gerar_sucessores(self, estado):
        sucessores = []
        simbolo = estado.simbolo()

        for i in range(3):
            for j in range(3):

                # expansão de influência
                if estado.tabuleiro[i][j] == ".":
                    novo = estado.copiar()
                    novo.tabuleiro[i][j] = simbolo
                    novo.jogador = estado.trocar_jogador()

                    sucessores.append(Aresta(novo, "expansao", 1, 1))

                # mudança de regime
                elif estado.tabuleiro[i][j] != simbolo:
                    if self.pode_mudar_regime(estado.tabuleiro, i, j, estado.jogador):
                        novo = estado.copiar()
                        novo.tabuleiro[i][j] = simbolo
                        novo.jogador = estado.trocar_jogador()

                        sucessores.append(Aresta(novo, "mudanca_regime", 3, 2))

        return sucessores
    

    def avaliar(self, estado):
        score = 0

        for i in range(3):
            for j in range(3):

                if estado.tabuleiro[i][j] == "E":
                    score += 1
                    if self.pode_mudar_regime(estado.tabuleiro, i, j, "URSS"):
                        score -= 2

                elif estado.tabuleiro[i][j] == "U":
                    score -= 1
                    if self.pode_mudar_regime(estado.tabuleiro, i, j, "EUA"):
                        score += 2

        return score

    def terminal(self, estado):
        return all("." not in linha for linha in estado.tabuleiro)





