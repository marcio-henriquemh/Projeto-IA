# Projeto Disciplina de Fundamentos de Inteligência Artificial
Aqui está a equipe principal:

**Equipe de Desenvolvimento**
- Marcos vinicius da silva santos
- Marcio Henrique Matos De Freitas

# ♟️ Minimax em Grafos com Sinais  
## Simulação Estrutural de Conflito Geopolítico (EUA vs URSS)


Este projeto modela um conflito estratégico entre duas superpotências utilizando:

- Teoria dos Jogos
- Grafos com Sinais
- Algoritmo Minimax
- Heurística Estrutural

O objetivo é demonstrar como Inteligência Artificial pode modelar decisões adversariais em um sistema polarizado.

---

# 🎯 Objetivo

Simular uma disputa territorial entre:

- 🇺🇸 EUA (MAX)
- 🇷🇺 URSS (MIN)

Ambos disputam influência sobre um território representado por uma grade 3×3.

Cada decisão é tomada assumindo que o adversário responderá da pior forma possível (modelo adversarial clássico).

---

# 🧠 Fundamentação Teórica

## 1️⃣ Jogo de Soma Zero

O ganho de um jogador representa a perda do outro:

U(EUA) = -U(URSS)

---

## 2️⃣ Representação como Grafo com Sinais

O território é modelado como:

G = (V, A, σ)

Onde:

- V = regiões (vértices)
- A = adjacências ortogonais
- σ(i,j) ∈ {+1, -1}

Definição de sinal:

- +1 → mesma potência (cooperação estrutural)
- -1 → potências rivais (conflito estrutural)

Isso permite medir:

- Coesão interna
- Instabilidade estrutural
- Polarização do sistema

---

## 3️⃣ Algoritmo Minimax

O algoritmo:

- Maximiza o valor estrutural para EUA
- Minimiza para URSS
- Avalia estados, não transições
- Assume resposta ótima do adversário

Não há soma acumulada de custos.

---

# 🗺️ Modelagem do Território

Cada estado é representado por:

T ∈ {E, U, .}^{3×3}

Onde:

- E → Influência EUA
- U → Influência URSS
- . → Região neutra

Estado do jogo:

s = (T, jogador_atual)

---

# ⚙️ Regras do Jogo

## 1️⃣ Expansão

O jogador pode ocupar uma região neutra.

---

## 2️⃣ Mudança de Regime

Uma região inimiga pode ser capturada se:

Possui ≥ 2 vizinhos controlados pelo jogador atual.

Interpretação:

- Pressão estrutural local
- Instabilidade ideológica
- Cercamento estratégico

---

# 📊 Função de Avaliação

A heurística combina:

### ✔ Controle Territorial
C(s) = |E| - |U|

### ✔ Centralidade Estratégica
Região central possui peso maior.

### ✔ Conectividade Estrutural
Vértices com mais aliados adjacentes têm maior valor.

### ✔ Penalização por Vulnerabilidade
Regiões cercadas são penalizadas.

Função final:

U(s) = Território + Conectividade + Centralidade - Vulnerabilidade

---

# 🔁 Melhorias Implementadas

## ✔ Quebra de Simetria

- Ordenação estrutural de sucessores
- Priorização por conectividade
- Desempate não determinístico controlado

Evita repetição mecânica de jogadas.

---

## ✔ Heurística Estrutural Refinada

Agora considera:

- Potencial local
- Vulnerabilidade topológica
- Valor posicional

---

# 📂 Estrutura do Projeto

projeto/
 ├── classe_ARESTAS.py  
 ├── classe_ESTADO.py  
 ├── classe_JOGO_TERRITORIAL.py  
 ├── classe_MINIMAX.py  
 ├── MINIMAX.py  
 └── README.md  

---

# Referências usadas
* [1] SOMBRA, J. V. F.; ANDRADE, R. C.; CAMPELO NETO, M. B. Desigualdades válidas para o problema do caminho positivo mínimo em digrafos de sinais. Fortaleza: UFC, 2025.
* Aulas da Disciplina de Fundamentos de IA- Professor: Hendrik Macedo
  
# ▶️ Como Executar

1️⃣ Clone o repositório:

```bash
git clone https://github.com/marcio-henriquemh/Projeto-IA.git
cd Projeto-IA
python MINIMAX.py


