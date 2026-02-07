# Parte 1 — Modelagem das Estruturas do Sistema

Este módulo corresponde à **Parte 1 do projeto** *Diplomacia da Segunda Guerra — Algoritmo Minimax*.

O objetivo desta etapa é **modelar corretamente as entidades fundamentais do sistema**, servindo como base para todas as etapas seguintes do algoritmo de busca competitiva e análise de grafos.

---

## 🎯 Objetivo da Parte 1

Definir, de forma clara e consistente, as estruturas que representam o cenário geopolítico:

- Países e seus respectivos blocos ideológicos.
- Relações diplomáticas (arestas do grafo).
- O estado global do jogo (nós da árvore de busca).

Nenhuma lógica de decisão de IA é implementada nesta fase inicial, apenas o esqueleto dos dados.

---

## 🧩 Entidades Modeladas

### 1️⃣ Estrutura de Relação

Representa o vínculo diplomático entre dois países. É o componente que sofre alteração durante as jogadas dos agentes.

Cada relação possui:

- `pais1`: Primeiro país da relação.
- `pais2`: Segundo país da relação.
- `sinal_peso`: Valor numérico da relação (positivo para aliança, negativo para conflito).

```python
class Estrutura_RELACAO:
    def __init__(self, pais1, pais2, sinal_peso):
        self.pais1 = pais1
        self.pais2 = pais2
        self.sinal_peso = sinal_peso
