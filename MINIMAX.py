import copy
import math
from classe_PAIS import Estrutura_PAIS
from classe_RELACOES import Estrutura_RELACAO
from classe_GRAFO import Estrutura_GRAFO
from classe_ESTADO import EstadoJogo

# Constantes
LIMITE_PROFUNDIDADE = 3  # Horizonte diplomático
ALIADOS = "ALIADOS"
EIXO = "EIXO"





# ETAPA 4 — Função Utilidade (atualizada)
def utilidade(estado, perspectiva="NEUTRA"):
    """
    Calcula a pontuação de utilidade para um estado do jogo.
    
    Args:
        estado: Estado atual do jogo
        perspectiva: "ALIADOS", "EIXO" ou "NEUTRA" (padrão)
        
    Returns:
        int: Pontuação calculada (positiva = bom para perspectiva)
    """
    pontuacao_aliados = 0
    pontuacao_eixo = 0
    
    for relacao in estado.grafo.lista_relacoes:
        p1 = relacao.pais1
        p2 = relacao.pais2
        peso = relacao.sinal_peso
        
        # Se são objetos PAIS, pega o nome
        if hasattr(p1, 'nome_pais'):
            nome1 = p1.nome_pais
            nome2 = p2.nome_pais
        else:
            nome1 = p1
            nome2 = p2
        
        # Verifica se ambos países são do mesmo bloco
        mesmo_bloco = estado.grafo.auxiliar_blocos(nome1, nome2)
        
        # Pontuação para ALIADOS
        if mesmo_bloco:
            if nome1 in estado.grafo.blocos["Aliados"]:  # São Aliados
                if peso > 0:
                    pontuacao_aliados += abs(peso)  # Aliança entre aliados é boa
                else:
                    pontuacao_aliados -= abs(peso)  # Conflito entre aliados é ruim
            else:  # São Eixo
                if peso > 0:
                    pontuacao_aliados -= abs(peso)  # Aliança entre eixo é ruim
                else:
                    pontuacao_aliados += abs(peso)  # Conflito entre eixo é bom
        else:  # Blocos opostos
            if peso < 0:  # Conflito entre blocos opostos
                pontuacao_aliados += abs(peso)  # É bom para Aliados
            else:  # Aliança entre blocos opostos
                pontuacao_aliados -= abs(peso)  # É ruim para Aliados
        
        # Pontuação para EIXO (lógica inversa)
        if mesmo_bloco:
            if nome1 in estado.grafo.blocos["Eixo"]:  # São Eixo
                if peso > 0:
                    pontuacao_eixo += abs(peso)  # Aliança entre eixo é boa
                else:
                    pontuacao_eixo -= abs(peso)  # Conflito entre eixo é ruim
            else:  # São Aliados
                if peso > 0:
                    pontuacao_eixo -= abs(peso)  # Aliança entre aliados é ruim
                else:
                    pontuacao_eixo += abs(peso)  # Conflito entre aliados é bom
        else:  # Blocos opostos
            if peso < 0:  # Conflito entre blocos opostos
                pontuacao_eixo -= abs(peso)  # É ruim para Eixo
            else:  # Aliança entre blocos opostos
                pontuacao_eixo += abs(peso)  # É bom para Eixo
    
    # Retorna baseado na perspectiva
    if perspectiva == "ALIADOS":
        return pontuacao_aliados
    elif perspectiva == "EIXO":
        return pontuacao_eixo
    else:  # NEUTRA - diferença entre os dois
        return pontuacao_aliados - pontuacao_eixo
    



# ETAPA 5 — Teste de Estado Terminal
def estado_terminal(estado):
    """Verifica se o estado é terminal"""
    return estado.profundidade >= LIMITE_PROFUNDIDADE

# ETAPA 6 — Função de alteração do peso
def aplicar_acao(relacao, jogador):
    """
    Aplica uma ação diplomática alterando o peso de uma relação
    
    Args:
        relacao: Objeto Estrutura_RELACAO
        jogador: "ALIADOS" ou "EIXO"
    """
    if jogador == ALIADOS:
        if relacao.sinal_peso >= 0:
            relacao.sinal_peso += 1   # fortalece aliança
        else:
            relacao.sinal_peso -= 1   # aumenta conflito (mais negativo)
    else:  # EIXO
        if relacao.sinal_peso >= 0:
            relacao.sinal_peso -= 1   # enfraquece aliança
        else:
            relacao.sinal_peso += 1   # reduz conflito (menos negativo)

# ETAPA 7 — Gerar Estados Sucessores
def gerar_sucessores(estado):
    """
    Gera todos os estados sucessores possíveis
    
    Args:
        estado: Estado atual do jogo
        
    Returns:
        list: Lista de estados sucessores
    """
    lista_sucessores = []
    
    # Para cada relação no grafo
    for i in range(len(estado.grafo.lista_relacoes)):
        # Cria uma cópia profunda do estado
        novo_estado = estado.copiar()
        
        # Obtém a relação específica
        rel = novo_estado.grafo.lista_relacoes[i]
        
        # Aplica a ação do jogador atual
        aplicar_acao(rel, estado.jogador_atual)
        
        # Determina próximo jogador
        if estado.jogador_atual == ALIADOS:
            proximo_jogador = EIXO
        else:
            proximo_jogador = ALIADOS
        
        # Atualiza o estado
        novo_estado.jogador_atual = proximo_jogador
        novo_estado.profundidade = estado.profundidade + 1
        
        # Adiciona à lista
        lista_sucessores.append(novo_estado)
    
    return lista_sucessores


# ETAPA 8 — Algoritmo MINIMAX
def minimax(estado, alpha=-math.inf, beta=math.inf):
    """
    Implementa o algoritmo Minimax com poda alpha-beta
    
    Args:
        estado: Estado atual do jogo
        alpha: Valor alpha para poda
        beta: Valor beta para poda
        
    Returns:
        int: Valor minimax do estado
    """
    # Caso terminal
    if estado_terminal(estado):
        # Cada jogador vê a utilidade de sua perspectiva
        if estado.jogador_atual == ALIADOS:
            return utilidade(estado, "NEUTRA")  # ALIADOS quer maximizar
        else:
            return utilidade(estado, "NEUTRA")  # EIXO quer minimizar
    
    # MAX (ALIADOS) - quer maximizar a pontuação
    if estado.jogador_atual == ALIADOS:
        melhor_valor = -math.inf
        sucessores = gerar_sucessores(estado)
        
        for sucessor in sucessores:
            valor = minimax(sucessor, alpha, beta)
            melhor_valor = max(melhor_valor, valor)
            alpha = max(alpha, melhor_valor)
            
            # Poda beta
            if beta <= alpha:
                break
        
        return melhor_valor
    
    # MIN (EIXO) - quer minimizar a pontuação (negativa para ALIADOS)
    else:
        pior_valor = math.inf
        sucessores = gerar_sucessores(estado)
        
        for sucessor in sucessores:
            valor = minimax(sucessor, alpha, beta)
            pior_valor = min(pior_valor, valor)
            beta = min(beta, pior_valor)
            
            # Poda alpha
            if beta <= alpha:
                break
        
        return pior_valor

def simular_partida_completa(estado_inicial, max_jogadas=6):
    """
    Simula uma partida completa entre ALIADOS e EIXO
    
    Args:
        estado_inicial: Estado inicial do jogo
        max_jogadas: Número máximo de jogadas
        
    Returns:
        dict: Resultado da partida
    """
    estado_atual = estado_inicial
    historico = []
    jogador_inicial = estado_inicial.jogador_atual
    
    print(f"\n🎮 INICIANDO PARTIDA: {jogador_inicial} começa")
    print("-" * 50)
    
    for jogada in range(max_jogadas):
        if estado_terminal(estado_atual):
            print(f"\n🏁 PARTIDA TERMINADA (limite de profundidade)")
            break
        
        # Determina quem joga
        jogador = estado_atual.jogador_atual
        
        # Encontra a melhor ação para o jogador atual
        if jogador == ALIADOS:
            melhor_estado, valor, acao_idx = melhor_acao(estado_atual)
        else:
            # Para o EIXO, queremos minimizar
            melhor_estado, valor, acao_idx = pior_acao(estado_atual)
        
        # Registra a jogada
        rel_original = estado_atual.grafo.lista_relacoes[acao_idx]
        rel_nova = melhor_estado.grafo.lista_relacoes[acao_idx]
        
        historico.append({
            'jogada': jogada + 1,
            'jogador': jogador,
            'acao': acao_idx,
            'relacao_antes': str(rel_original),
            'relacao_depois': str(rel_nova),
            'valor': valor,
            'utilidade_aliados': utilidade(melhor_estado, "ALIADOS"),
            'utilidade_eixo': utilidade(melhor_estado, "EIXO"),
            'utilidade_neutra': utilidade(melhor_estado, "NEUTRA")
        })
        
        # Mostra a jogada
        print(f"\nJogada {jogada + 1}: {jogador}")
        print(f"  Ação: Alterar relação [{acao_idx}]")
        print(f"  De: {rel_original}")
        print(f"  Para: {rel_nova}")
        print(f"  Variação: {rel_nova.sinal_peso - rel_original.sinal_peso:+d}")
        
        # Atualiza estado
        estado_atual = melhor_estado
    
    # Resultado final
    print("\n" + "=" * 50)
    print("🏆 RESULTADO FINAL")
    print("=" * 50)
    
    util_final_aliados = utilidade(estado_atual, "ALIADOS")
    util_final_eixo = utilidade(estado_atual, "EIXO")
    util_final_neutra = utilidade(estado_atual, "NEUTRA")
    
    print(f"\n📊 PONTUAÇÃO FINAL:")
    print(f"  ALIADOS: {util_final_aliados}")
    print(f"  EIXO: {util_final_eixo}")
    print(f"  DIFERENÇA: {util_final_neutra}")
    
    # Determina vencedor
    if util_final_neutra > 0:
        vencedor = "ALIADOS"
    elif util_final_neutra < 0:
        vencedor = "EIXO"
    else:
        vencedor = "EMPATE"
    
    print(f"\n🏆 VENCEDOR: {vencedor}")
    
    if vencedor == "ALIADOS":
        print("  ✓ Os Aliados dominaram a diplomacia!")
    elif vencedor == "EIXO":
        print("  ⚡ O Eixo conquistou a supremacia diplomática!")
    else:
        print("  🤝 Equilíbrio de poder mantido!")
    
    return {
        'estado_final': estado_atual,
        'vencedor': vencedor,
        'pontuacao_aliados': util_final_aliados,
        'pontuacao_eixo': util_final_eixo,
        'diferenca': util_final_neutra,
        'historico': historico
    }

def pior_acao(estado_inicial):
    """
    Encontra a pior ação para o adversário (usado pelo EIXO)
    
    Args:
        estado_inicial: Estado atual do jogo
        
    Returns:
        tuple: (pior_estado, pior_valor, indice_acao)
    """
    pior_valor = math.inf
    pior_estado = None
    pior_acao_idx = -1
    
    # Gera todos os sucessores (ações possíveis)
    sucessores = gerar_sucessores(estado_inicial)
    
    for i, sucessor in enumerate(sucessores):
        valor = minimax(sucessor)
        
        if valor < pior_valor:
            pior_valor = valor
            pior_estado = sucessor
            pior_acao_idx = i
    
    return pior_estado, pior_valor, pior_acao_idx


def criar_grafo_equilibrado():
    """Cria um grafo inicial equilibrado para ambos os lados"""
    relacoes = [
        # ALIADOS: 3 relações fortes
        Estrutura_RELACAO("EUA", "Reino Unido", 3),     # Aliança forte Aliados
        Estrutura_RELACAO("União Soviética", "EUA", 2), # Aliança média Aliados
        Estrutura_RELACAO("França", "Reino Unido", 2),  # Aliança média Aliados
        
        # EIXO: 3 relações fortes
        Estrutura_RELACAO("Alemanha", "Japão", 3),      # Aliança forte Eixo
        Estrutura_RELACAO("Itália", "Alemanha", 2),     # Aliança média Eixo
        Estrutura_RELACAO("Japão", "Itália", 2),        # Aliança média Eixo
        
        # Conflitos entre blocos (equilibrados)
        Estrutura_RELACAO("Alemanha", "EUA", -2),       # Conflito médio
        Estrutura_RELACAO("Japão", "Reino Unido", -1),  # Conflito leve
        
        # Relações neutras/mistas
        Estrutura_RELACAO("Itália", "França", 0),       # Neutra
        Estrutura_RELACAO("União Soviética", "Japão", -1), # Conflito leve
    ]
    
    blocos = {
        "Eixo": ["Alemanha", "Japão", "Itália"],
        "Aliados": ["Reino Unido", "EUA", "União Soviética", "França"]
    }
    
    return Estrutura_GRAFO(relacoes, blocos)

def analisar_equilibrio(estado):
    """Analisa o equilíbrio do estado atual"""
    util_aliados = utilidade(estado, "ALIADOS")
    util_eixo = utilidade(estado, "EIXO")
    diferenca = util_aliados - util_eixo
    
    print("\n⚖️  ANÁLISE DE EQUILÍBRIO:")
    print(f"  Força ALIADOS: {util_aliados}")
    print(f"  Força EIXO: {util_eixo}")
    print(f"  Vantagem: {diferenca:+d}")
    
    if abs(diferenca) <= 5:
        print("  📊 STATUS: EQUILIBRADO")
    elif diferenca > 5:
        print("  📊 STATUS: ALIADOS em vantagem")
    else:
        print("  📊 STATUS: EIXO em vantagem")
    
    return diferenca



# ETAPA 9 — Escolher a Melhor Decisão Diplomática
def melhor_acao(estado_inicial):
    """
    Encontra a melhor ação a partir do estado inicial
    
    Args:
        estado_inicial: Estado inicial do jogo
        
    Returns:
        tuple: (melhor_estado, melhor_valor, indice_acao)
    """
    melhor_valor = -math.inf
    melhor_estado = None
    melhor_acao_idx = -1
    
    # Gera todos os sucessores (ações possíveis)
    sucessores = gerar_sucessores(estado_inicial)
    
    for i, sucessor in enumerate(sucessores):
        valor = minimax(sucessor)
        
        if valor > melhor_valor:
            melhor_valor = valor
            melhor_estado = sucessor
            melhor_acao_idx = i
    
    return melhor_estado, melhor_valor, melhor_acao_idx

# Função auxiliar para criar grafo inicial
def criar_grafo_segunda_guerra():
    """Cria o grafo inicial com relações da Segunda Guerra"""
    relacoes = [
        Estrutura_RELACAO("Alemanha", "Japão", 2),      # Aliança Eixo-Eixo
        Estrutura_RELACAO("EUA", "Reino Unido", 3),     # Aliança Aliados-Aliados
        Estrutura_RELACAO("Alemanha", "EUA", -2),       # Conflito Eixo-Aliados
        Estrutura_RELACAO("Japão", "França", 0),        # Relação neutra
        Estrutura_RELACAO("Itália", "Alemanha", 2),     # Aliança Eixo-Eixo
        Estrutura_RELACAO("União Soviética", "EUA", 1), # Aliança Aliados-Aliados
    ]
    
    blocos = {
        "Eixo": ["Alemanha", "Japão", "Itália"],
        "Aliados": ["Reino Unido", "EUA", "União Soviética", "França"]
    }
    
    return Estrutura_GRAFO(relacoes, blocos)

# ETAPA FINAL — Execução Completa
def executar_jogo():
    """Executa o jogo completo"""
    print("\n" + "=" * 60)
    print("🎮 DIPLOMACIA DA SEGUNDA GUERRA - ALGORITMO MINIMAX")
    print("=" * 60)
    
    # Criar estado inicial
    grafo_inicial = criar_grafo_segunda_guerra()
    estado_inicial = EstadoJogo(
        grafo=grafo_inicial,
        jogador_atual=ALIADOS,
        profundidade=0
    )
    
    print("\n📋 ESTADO INICIAL:")
    print(f"  Jogador atual: {estado_inicial.jogador_atual}")
    print(f"  Profundidade: {estado_inicial.profundidade}/{LIMITE_PROFUNDIDADE}")
    print(f"  Número de relações: {len(estado_inicial.grafo.lista_relacoes)}")
    
    print("\n🌍 BLOCOS:")
    print(f"  • ALIADOS: {', '.join(estado_inicial.grafo.blocos['Aliados'])}")
    print(f"  • EIXO: {', '.join(estado_inicial.grafo.blocos['Eixo'])}")
    
    print("\n🤝 RELAÇÕES INICIAIS:")
    estado_inicial.grafo.exibir_grafo()
    
    utilidade_inicial = utilidade(estado_inicial)
    print(f"\n📊 PONTUAÇÃO INICIAL (utilidade): {utilidade_inicial}")
    print("   (Quanto maior, melhor para os ALIADOS)")
    
    print("\n🤔 ANALISANDO POSSÍVEIS DECISÕES...")
    print("   (Algoritmo Minimax em execução...)")
    
    melhor_estado, valor, acao_idx = melhor_acao(estado_inicial)
    
    print("\n" + "=" * 60)
    print("✅ RESULTADO - MELHOR DECISÃO DIPLOMÁTICA")
    print("=" * 60)
    
    print(f"\n🎯 VALOR ESPERADO DA DECISÃO: {valor}")
    print(f"📈 MELHORIA: {valor - utilidade_inicial} pontos")
    
    rel_original = estado_inicial.grafo.lista_relacoes[acao_idx]
    rel_nova = melhor_estado.grafo.lista_relacoes[acao_idx]
    
    print(f"\n🔄 AÇÃO ESCOLHIDA: Alterar relação [{acao_idx}]")
    print(f"   Relação: {rel_original}")
    print(f"   Nova relação: {rel_nova}")
    print(f"   Efeito: {rel_nova.sinal_peso - rel_original.sinal_peso:+d}")
    
    # Explicação da ação
    print(f"\n💡 EXPLICAÇÃO DA AÇÃO:")
    if rel_original.sinal_peso >= 0:
        if rel_nova.sinal_peso > rel_original.sinal_peso:
            print(f"   ALIADOS fortalecem uma aliança")
        else:
            print(f"   ALIADOS enfraquecem uma aliança")
    else:
        if rel_nova.sinal_peso < rel_original.sinal_peso:
            print(f"   ALIADOS intensificam um conflito")
        else:
            print(f"   ALIADOS reduzem um conflito")
    
    print(f"\n📊 NOVO ESTADO APÓS AÇÃO:")
    print(f"  Profundidade: {melhor_estado.profundidade}/{LIMITE_PROFUNDIDADE}")
    print(f"  Próximo jogador: {melhor_estado.jogador_atual}")
    print(f"  Nova pontuação: {utilidade(melhor_estado)}")
    
    print("\n🤝 RELAÇÕES ATUALIZADAS:")
    melhor_estado.grafo.exibir_grafo()
    
    # Análise de todas as opções
    print("\n" + "=" * 60)
    print("📈 ANÁLISE COMPARATIVA DE TODAS AS AÇÕES")
    print("=" * 60)
    
    sucessores = gerar_sucessores(estado_inicial)
    print("\nOpções disponíveis para ALIADOS:")
    print("Índice | Relação Original       | Ação            | Valor Esperado")
    print("-" * 65)
    
    for i, sucessor in enumerate(sucessores):
        valor_sucessor = minimax(sucessor)
        rel_orig = estado_inicial.grafo.lista_relacoes[i]
        rel_nova_s = sucessor.grafo.lista_relacoes[i]
        variacao = rel_nova_s.sinal_peso - rel_orig.sinal_peso
        
        # Formata a ação
        if variacao > 0:
            acao_desc = f"Fortalecer (+{variacao})"
        elif variacao < 0:
            acao_desc = f"Conflitar ({variacao})"
        else:
            acao_desc = "Manter"
        
        # Marca a melhor ação
        indicador = "★" if i == acao_idx else " "
        
        # CORREÇÃO: Converter para string antes de formatar
        rel_str = str(rel_orig)
        print(f"  {i:2d}{indicador} | {rel_str:22} | {acao_desc:15} | {valor_sucessor:4d}")
    
    print(f"\n★ = Melhor ação escolhida (índice {acao_idx})")
    
    return melhor_estado, valor

def analisar_relacao(estado, indice):
    """Faz uma análise detalhada de uma relação específica"""
    if 0 <= indice < len(estado.grafo.lista_relacoes):
        rel = estado.grafo.lista_relacoes[indice]
        
        print(f"\n🔍 ANÁLISE DETALHADA DA RELAÇÃO [{indice}]:")
        print(f"   Relação: {rel}")
        
        # Determinar tipo de relação
        if hasattr(rel.pais1, 'nome_pais'):
            nome1 = rel.pais1.nome_pais
            nome2 = rel.pais2.nome_pais
        else:
            nome1 = rel.pais1
            nome2 = rel.pais2
        
        # Verificar blocos
        mesmo_bloco = estado.grafo.auxiliar_blocos(nome1, nome2)
        
        if mesmo_bloco:
            if nome1 in estado.grafo.blocos["Aliados"]:
                tipo = "ALIADOS-ALIADOS"
                impacto = "Positivo" if rel.sinal_peso > 0 else "Negativo"
            else:
                tipo = "EIXO-EIXO"
                impacto = "Negativo" if rel.sinal_peso > 0 else "Positivo"
        else:
            tipo = "ALIADOS-EIXO"
            impacto = "Negativo" if rel.sinal_peso >= 0 else "Positivo"
        
        print(f"   Tipo: {tipo}")
        print(f"   Impacto para ALIADOS: {impacto}")
        print(f"   Valor atual: {rel.sinal_peso}")
        
        # Sugestão de ação
        if tipo == "ALIADOS-ALIADOS":
            print(f"   💡 Sugestão: Aumentar valor (fortalecer aliança)")
        elif tipo == "EIXO-EIXO":
            print(f"   💡 Sugestão: Diminuir valor (criar conflito)")
        elif tipo == "ALIADOS-EIXO":
            if rel.sinal_peso >= 0:
                print(f"   💡 Sugestão: Diminuir valor (enfraquecer aliança)")
            else:
                print(f"   💡 Sugestão: Aumentar conflito (valor mais negativo)")
        
        return tipo, impacto
    return None, None

# Função para mostrar explicação
def explicar_logica():
    print("\n" + "=" * 60)
    print("📚 EXPLICAÇÃO DA LÓGICA - DIPLOMACIA DA SEGUNDA GUERRA")
    print("=" * 60)
    print("\n🎯 OBJETIVO DO JOGO: Conduzir a diplomacia para favorecer seu bloco")
    print("   • Cada bloco busca maximizar seu poder diplomático")
    print("   • Vitória é determinada pela diferença de força no final")
    
    print("\n🎭 DOIS JOGADORES:")
    print("  1. 🤝 ALIADOS (Jogador MAX)")
    print("     • Países: Reino Unido, EUA, União Soviética, França")
    print("     • Objetivo: Maximizar a pontuação final")
    
    print("\n  2. ⚡ EIXO (Jogador MIN)")
    print("     • Países: Alemanha, Japão, Itália")
    print("     • Objetivo: Minimizar a pontuação final")
    
    print("\n📊 REGRAS DIPLOMÁTICAS (OBJETIVOS DE CADA BLOCO):")
    print("  Para os ALIADOS:")
    print("  1. ✅ ALIANÇA ENTRE ALIADOS: + (fortalecer coalizão)")
    print("  2. ✅ CONFLITO ALIADOS vs EIXO: + (enfraquecer inimigo)")
    print("  3. ❌ ALIANÇA ALIADOS com EIXO: - (evitar cooperação com inimigo)")
    print("  4. ❌ ALIANÇA ENTRE EIXO: - (impedir união inimiga)")
    
    print("\n  Para o EIXO (lógica inversa):")
    print("  1. ✅ ALIANÇA ENTRE EIXO: + (fortalecer aliança)")
    print("  2. ✅ CONFLITO EIXO vs ALIADOS: - (é ruim para o Eixo)")
    print("  3. ❌ ALIANÇA EIXO com ALIADOS: + (é bom infiltrar-se)")
    print("  4. ❌ ALIANÇA ENTRE ALIADOS: - (enfraquecer coalizão inimiga)")
    
    print("\n🎮 AÇÕES DIPLOMÁTICAS DISPONÍVEIS:")
    print("  • ALIADOS em seu turno:")
    print("     - Fortalecer alianças entre Aliados (aumentar peso positivo)")
    print("     - Intensificar conflitos com o Eixo (aumentar peso negativo)")
    print("     - Enfraquecer alianças do Eixo (diminuir peso positivo)")
    
    print("\n  • EIXO em seu turno:")
    print("     - Fortalecer alianças entre países do Eixo (aumentar peso positivo)")
    print("     - Reduzir conflitos com os Aliados (diminuir peso negativo)")
    print("     - Enfraquecer alianças dos Aliados (diminuir peso positivo)")
    
    print("\n⚖️  SISTEMA DE PONTUAÇÃO:")
    print("  • Pontuação final = Força_Aliados - Força_Eixo")
    print("  • Positiva: ALIADOS venceram")
    print("  • Negativa: EIXO venceu")
    print("  • Zero: EMPATE diplomático")
    
    print("\n⚙️  REGRAS DO JOGO:")
    print(f"  • Horizonte diplomático: {LIMITE_PROFUNDIDADE} níveis de profundidade")
    print("  • Cada jogada altera UMA relação específica")
    print("  • Turnos alternados: ALIADOS → EIXO → ALIADOS → ...")
    print("  • Valores das relações:")
    print("     +5 a +1: Forte aliança")
    print("       0: Relação neutra")
    print("     -1 a -5: Forte conflito")
    
    print("\n🤖 ALGORITMO MINIMAX ESTRATÉGICO:")
    print("  • ALIADOS (MAX): Escolhe ações que MAXIMIZAM a pontuação final")
    print("  • EIXO (MIN): Escolhe ações que MINIMIZAM a pontuação final")
    print("  • Considera todas as jogadas possíveis até o horizonte {LIMITE_PROFUNDIDADE}")
    print("  • Poda Alpha-Beta: Otimiza a busca cortando ramos irrelevantes")
    
    print("\n🏆 CONDIÇÃO DE VITÓRIA:")
    print("  • O vencedor é determinado pela PONTUAÇÃO FINAL após o limite de profundidade")
    print("  • AMBOS os lados têm chance real de vitória")
    print("  • Estratégia e antecipação são fundamentais")
    
    print("\n💡 EXEMPLO DE ESTRATÉGIA:")
    print("  Se ALIADOS estão perdendo, podem:")
    print("  1. Fortalecer aliança EUA-Reino Unido")
    print("  2. Aumentar conflito Alemanha-EUA")
    print("  3. Enfraquecer aliança Alemanha-Japão")
    
    print("\n  Se EIXO está perdendo, podem:")
    print("  1. Fortalecer aliança Alemanha-Itália")
    print("  2. Reduzir conflito Japão-França")
    print("  3. Enfraquecer aliança URSS-EUA")
    print("=" * 60)


# No início do arquivo principal, adicione:
VERSAO = "2.0 - Modo Competitivo"

def mostrar_cabecalho():
    print("\n" + "=" * 70)
    print(f"🎮 DIPLOMACIA DA SEGUNDA GUERRA - MINIMAX {VERSAO}")
    print("=" * 70)
    print("⚔️  UMA VERDADEIRA DISPUTA DIPLOMÁTICA ONDE AMBOS OS LADOS PODEM VENCER!")
    print("=" * 70)

def mostrar_placar(estado):
    """Mostra o placar atual do jogo"""
    aliados = utilidade(estado, "ALIADOS")
    eixo = utilidade(estado, "EIXO")
    diferenca = aliados - eixo
    
    print("\n📊 PLACAR ATUAL:")
    print(f"  🤝 ALIADOS: {aliados:3d} pontos")
    print(f"  ⚡ EIXO:    {eixo:3d} pontos")
    print(f"  ⚖️  DIFERENÇA: {diferenca:+3d} pontos")
    
    if diferenca > 0:
        print(f"  🏆 LIDERANÇA: ALIADOS (vantagem de {diferenca} pontos)")
    elif diferenca < 0:
        print(f"  🏆 LIDERANÇA: EIXO (vantagem de {-diferenca} pontos)")
    else:
        print(f"  ⚖️  LIDERANÇA: EMPATE PERFEITO")
    
    return diferenca

# Modifique a função principal:
if __name__ == "__main__":
    mostrar_cabecalho()
    explicar_logica()
    
    # Criar estado inicial equilibrado
    print("\n" + "=" * 60)
    print("⚖️  PREPARANDO CAMPO DE Batalha diplomática")
    print("=" * 60)
    
    grafo_inicial = criar_grafo_equilibrado()
    estado_inicial = EstadoJogo(grafo_inicial, ALIADOS, 0)
    
    print("\n📋 CONFIGURAÇÃO INICIAL:")
    mostrar_placar(estado_inicial)
    
    print("\n🤝 RELAÇÕES INICIAIS:")
    estado_inicial.grafo.exibir_grafo()
    
    # Perguntar quem começa
    print("\n🎲 CONFIGURAÇÃO DA PARTIDA:")
    print("1. ALIADOS começam (recomendado para primeiro teste)")
    print("2. EIXO começa (mais desafiador)")
    print("3. Aleatório")
    
    try:
        opcao = int(input("\nEscolha uma opção (1-3): "))
        if opcao == 1:
            estado_inicial.jogador_atual = ALIADOS
            print("✓ ALIADOS começam a partida!")
        elif opcao == 2:
            estado_inicial.jogador_atual = EIXO
            print("✓ EIXO começa a partida!")
        else:
            import random
            estado_inicial.jogador_atual = random.choice([ALIADOS, EIXO])
            print(f"✓ Sorteio: {estado_inicial.jogador_atual} começam!")
    except:
        print("✓ Usando padrão: ALIADOS começam")
        estado_inicial.jogador_atual = ALIADOS
    
    print(f"\n🎯 OBJETIVO: Conduzir a diplomacia para que seu bloco termine com")
    print("            MAIS PONTOS que o adversário!")
    
    input("\nPressione ENTER para iniciar a partida...")
    
    # Iniciar partida
    resultado = simular_partida_completa(estado_inicial, max_jogadas=6)
    
    # Resultado final
    print("\n" + "=" * 70)
    print("🏁 PARTIDA CONCLUÍDA!")
    print("=" * 70)
    
    if resultado['vencedor'] == "ALIADOS":
        print("\n🎉 VITÓRIA DOS ALIADOS!")
        print("   A coalizão democrática prevaleceu na diplomacia!")
    elif resultado['vencedor'] == "EIXO":
        print("\n⚡ VITÓRIA DO EIXO!")
        print("   As potências do Eixo dominaram as relações internacionais!")
    else:
        print("\n🤝 EMPATE DIPLOMÁTICO!")
        print("   Equilíbrio de poder mantido - a guerra continua!")
    
    print(f"\n📊 RESULTADO FINAL:")
    print(f"   ALIADOS: {resultado['pontuacao_aliados']} pontos")
    print(f"   EIXO:    {resultado['pontuacao_eixo']} pontos")
    print(f"   DIFERENÇA: {resultado['diferenca']:+d} pontos")
    
    # Mostrar histórico
    print("\n📜 HISTÓRICO DAS JOGADAS:")
    print("-" * 80)
    print("Jogada | Jogador | Ação | Relação (antes → depois) | Resultado")
    print("-" * 80)
    
    for jogada in resultado['historico']:
        print(f"{jogada['jogada']:6d} | {jogada['jogador']:7} | "
              f"{jogada['acao']:4d} | {jogada['relacao_antes']:>15} → {jogada['relacao_depois']:<15} | "
              f"{jogada['utilidade_neutra']:+4d}")
    
    print("\n✅ Jogo finalizado! O algoritmo Minimax foi executado com sucesso.")
    print("   Ambos os lados tiveram chance igual de vitória!")
# Execução principal
if __name__ == "__main__":
    explicar_logica()
    
    print("\n" + "=" * 60)
    print("🎮 MODO: DISPUTA COMPLETA (ALIADOS vs EIXO)")
    print("=" * 60)
    
    # Criar grafo equilibrado
    grafo_equilibrado = criar_grafo_equilibrado()
    
    print("\n📊 CONFIGURAÇÃO INICIAL EQUILIBRADA:")
    print("  • Cada bloco tem 3 alianças fortes/médias")
    print("  • Conflitos equilibrados entre blocos")
    print("  • Algumas relações neutras")
    
    # Testar quem começa primeiro
    print("\n🔬 TESTANDO DIFERENTES CENÁRIOS:")
    
    for jogador_inicial in [ALIADOS, EIXO]:
        print(f"\n{'='*40}")
        print(f"CENÁRIO: {jogador_inicial} começam")
        print('='*40)
        
        estado_inicial = EstadoJogo(
            grafo=grafo_equilibrado.copiar(),
            jogador_atual=jogador_inicial,
            profundidade=0
        )
        
        # Analisar equilíbrio inicial
        analisar_equilibrio(estado_inicial)
        
        # Simular partida
        resultado = simular_partida_completa(estado_inicial, max_jogadas=4)
        
        # Resumo do cenário
        print(f"\n📋 RESUMO DO CENÁRIO ({jogador_inicial} começaram):")
        print(f"  Vencedor: {resultado['vencedor']}")
        print(f"  Pontuação final - ALIADOS: {resultado['pontuacao_aliados']}")
        print(f"  Pontuação final - EIXO: {resultado['pontuacao_eixo']}")
        print(f"  Diferença: {resultado['diferenca']:+d}")
    
    # Teste adicional: quem tem vantagem inicial
    print("\n" + "=" * 60)
    print("🎯 QUEM TEM MAIS CHANCE DE VENCER?")
    print("=" * 60)
    
    num_simulacoes = 10
    vitorias_aliados = 0
    vitorias_eixo = 0
    empates = 0
    
    print(f"\nSimulando {num_simulacoes} partidas rápidas...")
    
    for i in range(num_simulacoes):
        # Alterna quem começa
        jogador_inicial = ALIADOS if i % 2 == 0 else EIXO
        
        estado = EstadoJogo(
            grafo=criar_grafo_equilibrado(),
            jogador_atual=jogador_inicial,
            profundidade=0
        )
        
        # Jogada rápida (apenas 2 jogadas cada)
        for _ in range(4):  # 2 jogadas por jogador
            if estado.jogador_atual == ALIADOS:
                melhor_estado, _, _ = melhor_acao(estado)
            else:
                melhor_estado, _, _ = pior_acao(estado)
            estado = melhor_estado
        
        # Verifica vencedor
        util_final = utilidade(estado, "NEUTRA")
        if util_final > 0:
            vitorias_aliados += 1
        elif util_final < 0:
            vitorias_eixo += 1
        else:
            empates += 1
    
    print(f"\n📊 RESULTADO DAS {num_simulacoes} SIMULAÇÕES:")
    print(f"  Vitórias ALIADOS: {vitorias_aliados}")
    print(f"  Vitórias EIXO: {vitorias_eixo}")
    print(f"  Empates: {empates}")
    
    if vitorias_aliados > vitorias_eixo:
        print("  🏆 CONCLUSÃO: ALIADOS têm leve vantagem")
    elif vitorias_eixo > vitorias_aliados:
        print("  ⚡ CONCLUSÃO: EIXO têm leve vantagem")
    else:
        print("  ⚖️  CONCLUSÃO: Equilíbrio perfeito")
    
    print("\n✅ Sistema de disputa implementado com sucesso!")
    print("   Ambos os lados têm chance real de vitória!")