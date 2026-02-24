class Estado:
    def __init__(self, tabuleiro=None, jogador="EUA"):
        if tabuleiro is None:
            self.tabuleiro = [["." for _ in range(5)] for _ in range(5)]
        else:
            self.tabuleiro = tabuleiro

        self.jogador = jogador  # "EUA" ou "URSS"

    def copiar(self):
        novo_tab = [linha[:] for linha in self.tabuleiro]
        return Estado(novo_tab, self.jogador)

    def trocar_jogador(self):
        return "URSS" if self.jogador == "EUA" else "EUA"

    def simbolo(self):
        return "E" if self.jogador == "EUA" else "U"

    
    
    def mostrar(self):
        print("Mapa de Influencia:")
        for linha in self.tabuleiro:
            print(linha)
        print()