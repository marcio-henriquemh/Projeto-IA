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

class Maquina:
    #construtor
    def __init__(self,id,estado,tempo_restante=0):       
        self.id=id
        self.estado=estado
        self.tempo_restante=tempo_restante 
      

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

'''
PARTE 2 — Funções Básicas do Sistema

Objetivo desta parte
Implementar funções independentes do Minimax, que:

detectam quando o sistema terminou

avaliam a qualidade de um estado

Essas funções não tomam decisões, apenas medem o estado.

-Verificação de Estado Terminal
Ideia:O sistema terminou quando todos os processos estão no estado concluído.


-Função de Avaliação do Estado

Avaliar o quão ruim ou bom está o escalonamento atual, considerando:

tempo total acumulado

atrasos ponderados pela prioridade

Quanto maior o valor retornado, melhor o estado para o sistema (MAX).


'''


def estado_terminal(estado):
    for processo in estado.lista_processos:
        if processo.estado != "concluido":
            return False
    return True


def funcao_avaliar(estado,lambd=1.0):
    penalidade=0

    for processo in estado.lista_processos:
        atraso=processo.tempo_atual- processo.tempo_base
        if atraso >0:
            penalidade=penalidade+processo.prioridade*atraso
        return -(estado.tempo_total +  lambd* penalidade)


#testando criando objeto
p1 = Processo(1, 5, 5, 2, "concluido")
m1 = Maquina(1, "livre")
estado = Estado([p1], [m1], 0)
#testando funcionalidade 1(estado terminal)
p1.estado="concluido"
print(estado_terminal(estado))  # deve retornar True

#testando funcionalidade 2( funcao avaliar)
estado.tempo_total = 10
p1.tempo_base = 5
p1.tempo_atual = 7
p1.prioridade = 2

print(funcao_avaliar(estado))  # valor negativo, coerente com atraso





