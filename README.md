# Parte 1 — Modelagem das Estruturas do Sistema

Este módulo corresponde à **Parte 1 do projeto** *Minimax aplicado ao Escalonamento de Tarefas sob Sabotagem*.

O objetivo desta etapa é **modelar corretamente as entidades fundamentais do sistema**, servindo como base para todas as etapas seguintes do algoritmo Minimax.

---

## 🎯 Objetivo da Parte 1

Definir, de forma clara e consistente, as estruturas que representam:

- Processos da linha de produção
- Máquinas disponíveis
- Estado global do sistema produtivo

Nenhuma lógica de decisão é implementada nesta fase.

---

## 🧩 Entidades Modeladas

### 1️⃣ Processo

Representa uma tarefa da linha de produção.

Cada processo possui:

- `id`: identificador único  
- `tempo_base`: tempo de execução esperado  
- `tempo_atual`: tempo efetivo de execução (pode ser alterado por sabotagem)  
- `prioridade`: peso do processo na função de avaliação  
- `estado`: situação atual do processo  

Estados possíveis:
- `pendente`
- `executando`
- `concluído`

```python
class Processo:
    def __init__(self, id, tempo_base, tempo_atual, prioridade, estado):
        self.id = id
        self.tempo_base = tempo_base
        self.tempo_atual = tempo_atual
        self.prioridade = prioridade
        self.estado = estado
