'''
Parte 1 -Modelagem das estruturas do sistema


ESTRUTURA Processo:
    id
    tempo_base
    tempo_atual
    prioridade
    estado        // pendente, executando, concluído
'''

class Processo:
    #construtor
    def __init__(self, id,tempo_base,tempo_atual,prioridade,estado):
        self.id=id
        self.tempo_base=tempo_base
        self.tempo_atual=tempo_atual
        self.estado=estado
        self.prioridade=prioridade
    

'método de acessos se necessário'

def tempo_atual(self, novo_tempo):
        if novo_tempo < 0:
            print("Erro: Tempo não pode ser negativo.")
        elif novo_tempo > self.tempo_base:
            print("Erro: Tempo atual excede o tempo base.")
        else:
            self._tempo_atual = novo_tempo
