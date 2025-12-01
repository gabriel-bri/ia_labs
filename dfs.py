import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from estado import Estado


class BuscaProfundidade:    
    def __init__(self, grafo, cidade_inicial=0):
        self.grafo = grafo
        self.num_cidades = len(grafo)
        self.cidade_inicial = cidade_inicial
        
        # Métricas
        self.nos_gerados = 0
        self.nos_expandidos = 0
        self.tempo_execucao = 0
        
        # Solução
        self.melhor_custo = None
        self.melhor_caminho = None
    
    def expandir(self, estado):
        """
        Expande um estado gerando seus sucessores.
        
        Para cada cidade não visitada, cria um novo estado.
        """
        self.nos_expandidos += 1
        sucessores = []
        
        # Cidades não visitadas
        nao_visitadas = set(range(self.num_cidades)) - set(estado.visitadas)
        
        # Gera um sucessor para cada cidade não visitada
        for proxima in nao_visitadas:
            novas_visitadas = set(estado.visitadas) | {proxima}
            novo_caminho = estado.caminho + [proxima]
            custo_aresta = self.grafo[estado.cidade_atual][proxima]
            novo_custo = estado.custo + custo_aresta
            
            novo_estado = Estado(proxima, novas_visitadas, novo_caminho, novo_custo)
            sucessores.append(novo_estado)
            self.nos_gerados += 1
        
        return sucessores
    
    def buscar(self):
        inicio = time.time()
        
        # Estado inicial
        inicial = Estado(
            cidade_atual=self.cidade_inicial,
            visitadas={self.cidade_inicial},
            caminho=[self.cidade_inicial],
            custo=0
        )
        
        pilha = [inicial]
        
        # Melhor solução
        melhor = None
        melhor_custo = float('inf')
        
        # Loop principal
        while pilha:
            # Remove do topo da pilha
            estado = pilha.pop()
            
            # Teste de objetivo: visitou todas as cidades?
            if estado.ja_visitei_todas(self.num_cidades):
                # Custo total (inclui volta ao início)
                custo_volta = self.grafo[estado.cidade_atual][self.cidade_inicial]
                custo_total = estado.custo + custo_volta
                
                # Atualiza se for melhor
                if custo_total < melhor_custo:
                    melhor_custo = custo_total
                    melhor = estado
                
                continue
            
            # Expande e adiciona sucessores na pilha
            for sucessor in self.expandir(estado):
                pilha.append(sucessor)
        
        # Finaliza
        self.tempo_execucao = time.time() - inicio
        
        if melhor:
            self.melhor_custo = melhor_custo
            self.melhor_caminho = melhor.caminho + [self.cidade_inicial]
        
        return melhor
    
    def imprimir_resultados(self):
        """Imprime resultados da busca"""
        print("\n" + "="*70)
        print("BUSCA EM PROFUNDIDADE (DFS) - RESULTADOS")
        print("="*70)
        
        print(f"\nMÉTRICAS:")
        print(f"  Nós gerados:     {self.nos_gerados:,}")
        print(f"  Nós expandidos:  {self.nos_expandidos:,}")
        print(f"  Tempo:           {self.tempo_execucao:.4f} segundos")
        
        if self.melhor_caminho:
            print(f"\nSOLUÇÃO ENCONTRADA:")
            print(f"  Custo total:     {self.melhor_custo}")
            print(f"  Caminho:         {' -> '.join(map(str, self.melhor_caminho))}")
            
            print(f"\n  Detalhes do caminho:")
            for i in range(len(self.melhor_caminho) - 1):
                origem = self.melhor_caminho[i]
                destino = self.melhor_caminho[i + 1]
                dist = self.grafo[origem][destino]
                print(f"    [{origem}] --({dist})--> [{destino}]")
        else:
            print("\n  Nenhuma solução encontrada")
        
        print("="*70)
