from classe_processo import Processo
from classe_maquina import Maquina
from classe_estado import Estado
import copy      





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




'''
Parte 3

Geração de Estados Sucessores (Ações do Sistema)

No nosso estado, quais as opção pode ser tomadas a partir dele


-Temos máquinas

-Temos processos pendentes

-Uma ação = atribuir um processo a uma máquina livre

NÓ=ESTADO
ARESTA=AÇÃO
'''

def maquinas_livres(estado):
    livres = []
    for maquina in estado.lista_maquinas:
        if maquina.estado == "livre":
            livres.append(maquina)
    return livres

def processos_pendentes(estado):
    pendentes = []
    for processo in estado.lista_processos:
        if processo.estado == "pendente":
            pendentes.append(processo)
    return pendentes



#Cada decisão gera um novo mundo possível.
def clonar_estado(estado):
    return copy.deepcopy(estado)


def aplicar_acao(estado, processo, maquina):
    novo_estado = clonar_estado(estado)

    # localizar objetos clonados
    p = next(p for p in novo_estado.lista_processos if p.id == processo.id)
    m = next(m for m in novo_estado.lista_maquinas if m.id == maquina.id)

    # aplicar decisão
    p.estado = "executando"
    m.estado = "ocupada"
    m.tempo_restante = p.tempo_atual

    return novo_estado

def gerar_sucessores(estado):
    sucessores = []

    livres = maquinas_livres(estado)
    pendentes = processos_pendentes(estado)

    for maquina in livres:
        for processo in pendentes:
            novo_estado = aplicar_acao(estado, processo, maquina)
            sucessores.append(novo_estado)

    return sucessores



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



#PARTE 3
# Criando processo
p1 = Processo(1, 5, 5, 1, "pendente")

# Criando máquina
m1 = Maquina(1, "livre", 0)

# Criando estado inicial
estado_inicial = Estado(
    lista_processos=[p1],
    lista_maquinas=[m1],
    tempo_total=0
)

# Gerando sucessores
sucessores = gerar_sucessores(estado_inicial)

print("Quantidade de sucessores:", len(sucessores))

for i, e in enumerate(sucessores):
    print(f"\nSucessor {i+1}")
    for p in e.lista_processos:
        print(f"Processo {p.id} - estado: {p.estado}")
    for m in e.lista_maquinas:
        print(f"Máquina {m.id} - estado: {m.estado}, tempo restante: {m.tempo_restante}")



