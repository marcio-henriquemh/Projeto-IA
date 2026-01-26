
'Estados'

class Estado:
    def __init__(self, lista_processos=None, lista_maquinas=None, tempo_total=0):

        if lista_processos is None:
            self.lista_processos = []
        else:
            self.lista_processos = lista_processos

        if lista_maquinas is None:
            self.lista_maquinas = []
        else:
            self.lista_maquinas = lista_maquinas

        self.tempo_total = tempo_total
