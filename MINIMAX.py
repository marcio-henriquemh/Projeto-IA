from classe_ARESTAS import Aresta
from classe_ESTADO import Estado
from classe_MINIMAX import Minimax
from classe_JOGO_TERRITORIAL import GuerraFria

def main():
    jogo = GuerraFria()
    estado = Estado()
    minimax = Minimax(jogo, profundidade=3)

    rodada = 1
    while not jogo.terminal(estado):

        print("Rodada", rodada, "| Superpotência:", estado.jogador)
        estado.mostrar()

        melhor = minimax.melhor_jogada(estado)

        if melhor is None:
            break

        print("→ Jogada escolhida:", melhor.tipo)

        estado = melhor.estado_destino
        rodada += 1

    print("Resultado final da disputa:")
    estado.mostrar()
    print("Equilíbrio geopolítico:", jogo.avaliar(estado))


if __name__ == "__main__":
    main()