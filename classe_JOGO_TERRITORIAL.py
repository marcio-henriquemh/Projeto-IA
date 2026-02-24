from classe_ARESTAS import Aresta
import random
class GuerraFria:
    
    # VIZINHANÇA  5x5)
    def adjacentes(self, i, j):
        possiveis = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
        return [(x,y) for x,y in possiveis if 0 <= x < 5 and 0 <= y < 5]


    # VERIFICA VULNERABILIDADE
    # Uma região é vulnerável quando está estruturalmente exposta ao adversário
    def vulneravel(self, tabuleiro, i, j, simbolo):
        inimigo = "U" if simbolo == "E" else "E"
        contador = 0
        for x, y in self.adjacentes(i, j):
            if tabuleiro[x][y] == inimigo:
                contador += 1
        return contador >= 2


    # POTENCIAL ESTRUTURAL
    #potencial local é o número de aliados adjacentes, indicando a força de uma posição

    def potencial_local(self, tabuleiro, i, j, simbolo):
        aliados = 0
        for x, y in self.adjacentes(i, j):
            if tabuleiro[x][y] == simbolo:
                aliados += 1
        return aliados


    # gera todas as jogadas possíveis, atribuindo um peso baseado no potencial local e na vulnerabilidade, e ordena para priorizar as melhores opções
    def gerar_sucessores(self, estado):
        sucessores = []
        simbolo = estado.simbolo()
        inimigo = "U" if simbolo == "E" else "E"

        for i in range(5):
            for j in range(5):
                # EXPANSÃO (Colocar influência em um território vazio)
                if estado.tabuleiro[i][j] == ".":
                    novo = estado.copiar()
                    novo.tabuleiro[i][j] = simbolo
                    novo.jogador = estado.trocar_jogador()
                    peso = self.potencial_local(novo.tabuleiro, i, j, simbolo)
                    sucessores.append((peso, Aresta(novo, "expansao")))

                # MUDANÇA DE REGIME (Capturar território adversário se vulnerável)
                elif estado.tabuleiro[i][j] == inimigo:
                    if self.vulneravel(estado.tabuleiro, i, j, inimigo):
                        novo = estado.copiar()
                        novo.tabuleiro[i][j] = simbolo
                        novo.jogador = estado.trocar_jogador()
                        # Bônus de +2 para capturas estratégicas, incentivando o Minimax a priorizar essas jogadas
                        peso = self.potencial_local(novo.tabuleiro, i, j, simbolo) + 2
                        sucessores.append((peso, Aresta(novo, "mudanca_regime")))

        # Ordenação e aleatoriedade preservadas
        sucessores.sort(key=lambda x: x[0], reverse=True)
        sucessores = [a for (_, a) in sucessores]

        if len(sucessores) > 1:
            melhores = sucessores[:2]
            escolhido = random.choice(melhores)
            return [escolhido] + sucessores[2:]
        return sucessores

    
    # FUNÇÃO HEURÍSTICA -- Avaliação do estado
    # A avaliação considera o número de territórios controlados, a centralidade estratégica e a vulnerabilidade, atribuindo pesos para cada fator para refletir sua importância relativa no equilíbrio geopolítico.

    def avaliar(self, estado):
        score = 0
        # Mudado para range(4)
        for i in range(5):
            for j in range(5):
                if estado.tabuleiro[i][j] == "E":
                    score += 1
                # Bônus para posições centrais, incentivando o controle do centro do tabuleiro
                    if i in [1, 2] and j in [1, 2]:
                        score += 0.75
                    score += 0.3 * self.potencial_local(estado.tabuleiro, i, j, "E")
                    if self.vulneravel(estado.tabuleiro, i, j, "E"):
                        score -= 1.5
                elif estado.tabuleiro[i][j] == "U":
                    score -= 1
                    if i in [1, 2] and j in [1, 2]:
                        score -= 0.75
                    score -= 0.3 * self.potencial_local(estado.tabuleiro, i, j, "U")
                    if self.vulneravel(estado.tabuleiro, i, j, "U"):
                        score += 1.5
        return score


    # ESTADO TERMINAL- O jogo termina quando o tabuleiro está completamente preenchido, indicando que ambas as superpotências alcançaram um equilíbrio geopolítico total, ou seja, não há mais territórios vazios para conquistar ou defender, simbolizando o auge da tensão e da competição entre as duas potências.
    def terminal(self, estado):
        return all("." not in linha for linha in estado.tabuleiro)