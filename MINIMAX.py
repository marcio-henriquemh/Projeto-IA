
from classe_RELACOES import Estrutura_RELACAO
from classe_PAIS import Estrutura_PAIS
from classe_GRAFO import Estrutura_GRAFO

if __name__ == "__main__":
    # 1. Criar objetos PAIS
    p1 = Estrutura_PAIS("Brasil") # Usar o nome da CLASSE
    p2 = Estrutura_PAIS("Argentina")
    p3 = Estrutura_PAIS("Chile")
    
    # 2. Criar objetos RELACAO
    rel1 = Estrutura_RELACAO(p1, p2, "+") # Brasil + Argentina
    rel2 = Estrutura_RELACAO(p2, p3, "-") # Argentina - Chile
    
    # 3. Criar o GRAFO com as relações
    lista_de_relacoes = [rel1, rel2]
    meu_grafo = Estrutura_GRAFO(lista_de_relacoes)
    
    # 4. Testar a saída
    print("Teste Inicializado...")
    # Se Estrutura_GRAFO não tiver o método exibir_grafo, isso dará AttributeError
    # meu_grafo.exibir_grafo() 
    print("Relações criadas com sucesso.")