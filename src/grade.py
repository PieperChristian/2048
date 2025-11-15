#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Implementa a lógica central do jogo 2048: movimentação, fusão, pontuação e undo."""

import random
import copy

class Grade:
    """
    Gerencia toda a lógica interna do jogo 2048.
    
    Esta classe é responsável pela mecânica core do jogo, incluindo
    movimentação, fusão de peças, pontuação e controle de estado.
    
    Atributos:
    ---------
    tamanho : int
        Dimensão da grade (normalmente 4 para 4x4)
    matriz : list[list[int]]
        Matriz bidimensional representando o tabuleiro
        - 0 representa célula vazia
        - 2, 4, 8, ... representam valores das peças
    pontuacao : int
        Pontuação acumulada durante o jogo
    matriz_desfazer : list[list[int]] ou None
        Cópia da matriz antes do último movimento (para undo)
    pontuacao_desfazer : int
        Pontuação antes do último movimento (para undo)
    pode_desfazer : bool
        Flag indicando se o desfazer está disponível
    
    Métodos Públicos:
    ----------------
    salvar_estado_desfazer()
        Salva estado atual para possível undo
    carregar_estado_desfazer()
        Restaura estado salvo (undo)
    gerar_nova_peca()
        Adiciona nova peça (2 ou 4) em posição aleatória vazia
    pode_mover()
        Verifica se há movimentos possíveis (game over check)
    mover_esquerda(), mover_direita(), mover_cima(), mover_baixo()
        Executa movimento na direção especificada
    maior_peca()
        Retorna o valor da maior peça no tabuleiro
    
    Métodos Privados:
    ----------------
    _mover_linha_esquerda(linha)
        Função auxiliar que implementa o algoritmo de movimento
        para uma única linha
    \"\"\"
    >>> if not grade.pode_mover():
    ...     print("Game Over!")
    """
    
    def __init__(self, tamanho=4):
        """Inicializa grade zerada com duas peças iniciais aleatórias."""
        self.tamanho = tamanho
        # Inicializa a matriz (grid) com zeros
        self.matriz = [[0] * tamanho for _ in range(tamanho)]
        self.pontuacao = 0
        # Variáveis para a função 'desfazer'
        self.matriz_desfazer = None
        self.pontuacao_desfazer = 0
        self.pode_desfazer = False
        # Gera as duas primeiras peças
        self.gerar_nova_peca()
        self.gerar_nova_peca()

    def salvar_estado_desfazer(self):
        """Salva estado atual (deepcopy) para função desfazer."""
        # copy.deepcopy é essencial para criar uma cópia independente
        self.matriz_desfazer = copy.deepcopy(self.matriz)
        self.pontuacao_desfazer = self.pontuacao
        self.pode_desfazer = True

    def carregar_estado_desfazer(self):
        """Restaura estado salvo se disponível (uma vez apenas)."""
        if self.pode_desfazer:
            self.matriz = copy.deepcopy(self.matriz_desfazer)
            self.pontuacao = self.pontuacao_desfazer
            self.pode_desfazer = False # Só pode desfazer uma vez

    def gerar_nova_peca(self):
        """Gera nova peça (2 ou 4) em célula vazia aleatória."""
        celulas_vazias = []
        for r in range(self.tamanho):
            for c in range(self.tamanho):
                if self.matriz[r][c] == 0:
                    celulas_vazias.append((r, c))

        if celulas_vazias:
            r, c = random.choice(celulas_vazias)
            # 90% de chance de ser 2, 10% de chance de ser 4
            self.matriz[r][c] = 4 if random.random() < 0.1 else 2

    def pode_mover(self):
        """Verifica se há movimentos possíveis (células vazias ou fusões adjacentes)."""
        # 1. Verifica se há células vazias
        for r in range(self.tamanho):
            for c in range(self.tamanho):
                if self.matriz[r][c] == 0:
                    return True
        
        # 2. Verifica se há fusões possíveis (adjacentes)
        for r in range(self.tamanho):
            for c in range(self.tamanho):
                # Verifica horizontal
                if c < self.tamanho - 1 and self.matriz[r][c] == self.matriz[r][c+1]:
                    return True
                # Verifica vertical
                if r < self.tamanho - 1 and self.matriz[r][c] == self.matriz[r+1][c]:
                    return True
        
        return False # Sem movimentos possíveis

    def _mover_linha_esquerda(self, linha):
        """Move e funde uma linha para esquerda (compressão, fusão, preenchimento)."""
        nova_linha = [i for i in linha if i != 0] # 1. Comprimir (remove zeros)
        pontos_ganhos = 0
        
        # 2. Fundir
        i = 0
        while i < len(nova_linha) - 1:
            if nova_linha[i] == nova_linha[i+1]:
                valor_fundido = nova_linha[i] * 2
                nova_linha[i] = valor_fundido
                nova_linha.pop(i+1)
                pontos_ganhos += valor_fundido
            i += 1
            
        # 3. Preencher com zeros à direita
        while len(nova_linha) < self.tamanho:
            nova_linha.append(0)
            
        return nova_linha, pontos_ganhos

    def mover_esquerda(self):
        """Move todas as peças para esquerda. Retorna True se houve mudança."""
        mudou = False
        pontos_ganhos = 0
        nova_matriz = []
        for r in range(self.tamanho):
            linha_original = self.matriz[r]
            nova_linha, pontos = self._mover_linha_esquerda(linha_original)
            nova_matriz.append(nova_linha)
            pontos_ganhos += pontos
            if linha_original != nova_linha:
                mudou = True
                
        self.matriz = nova_matriz
        self.pontuacao += pontos_ganhos
        return mudou

    def mover_direita(self):
        """Move para direita (inverte, move esquerda, desinverte)."""
        mudou = False
        pontos_ganhos = 0
        nova_matriz = []
        for r in range(self.tamanho):
            linha_original = self.matriz[r]
            linha_invertida = linha_original[::-1] # Inverte
            nova_linha_invertida, pontos = self._mover_linha_esquerda(linha_invertida) # Move esquerda
            nova_matriz.append(nova_linha_invertida[::-1]) # Desinverte
            pontos_ganhos += pontos
            if linha_original != nova_matriz[-1]:
                mudou = True
                
        self.matriz = nova_matriz
        self.pontuacao += pontos_ganhos
        return mudou

    def mover_cima(self):
        """Move para cima (transpõe, move esquerda, transpõe de volta)."""
        mudou = False
        pontos_ganhos = 0
        # Transpõe a matriz (linhas viram colunas)
        matriz_transposta = [list(col) for col in zip(*self.matriz)]
        nova_matriz_transposta = []
        
        for c in range(self.tamanho):
            coluna_original = matriz_transposta[c]
            nova_coluna, pontos = self._mover_linha_esquerda(coluna_original) # Move "esquerda" (que é cima)
            nova_matriz_transposta.append(nova_coluna)
            pontos_ganhos += pontos
            if coluna_original != nova_coluna:
                mudou = True
                
        # Transpõe de volta ao normal
        self.matriz = [list(lin) for lin in zip(*nova_matriz_transposta)]
        self.pontuacao += pontos_ganhos
        return mudou

    def mover_baixo(self):
        """Move para baixo (transpõe, inverte, move esquerda, desinverte, transpõe)."""
        mudou = False
        pontos_ganhos = 0
        matriz_transposta = [list(col) for col in zip(*self.matriz)]
        nova_matriz_transposta = []
        
        for c in range(self.tamanho):
            coluna_original = matriz_transposta[c]
            coluna_invertida = coluna_original[::-1] # Inverte
            nova_coluna_invertida, pontos = self._mover_linha_esquerda(coluna_invertida) # Move "esquerda" (que é baixo)
            nova_matriz_transposta.append(nova_coluna_invertida[::-1]) # Desinverte
            pontos_ganhos += pontos
            if coluna_original != nova_matriz_transposta[-1]:
                mudou = True
                
        self.matriz = [list(lin) for lin in zip(*nova_matriz_transposta)]
        self.pontuacao += pontos_ganhos
        return mudou

    def maior_peca(self):
        """Retorna o valor da maior peça na grade."""
        maior = 0
        for linha in self.matriz:
            if max(linha) > maior:
                maior = max(linha)
        return maior