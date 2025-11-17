#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Funções utilitárias de renderização reutilizáveis (DRY)."""

import pygame
from src.configuracoes import *

def desenhar_fundo(tela):
    """ Desenha o fundo da grade (os quadrados cinzas vazios). """
    y_offset = 100 # Onde a grade começa no eixo Y (após o HUD superior)
    for r in range(TAMANHO_GRADE):
        for c in range(TAMANHO_GRADE):
            x = c * (TAMANHO_PECA + MARGEM_PECA) + MARGEM_PECA
            y = r * (TAMANHO_PECA + MARGEM_PECA) + MARGEM_PECA + y_offset
            pygame.draw.rect(tela, CORES[0], (x, y, TAMANHO_PECA, TAMANHO_PECA), border_radius=5)

def desenhar_peca(tela, valor, x, y, fontes_pecas):
    """ Desenha uma única peça na posição (x, y) com o valor dado. """
    cor_fundo = CORES.get(valor, CORES[2048]) # Pega a cor, ou a cor de 2048 se for maior
    cor_texto = CORES['texto_escuro'] if valor <= 4 else CORES['texto_claro']
    
    pygame.draw.rect(tela, cor_fundo, (x, y, TAMANHO_PECA, TAMANHO_PECA), border_radius=5)
    
    # Escolhe a fonte baseada no número de dígitos
    s_valor = str(valor)
    fonte = fontes_pecas.get(len(s_valor), fontes_pecas[4]) # Usa a fonte 4 para 5+ dígitos
    
    texto_surf = fonte.render(s_valor, True, cor_texto)
    texto_rect = texto_surf.get_rect(center=(x + TAMANHO_PECA / 2, y + TAMANHO_PECA / 2))
    tela.blit(texto_surf, texto_rect)

def desenhar_grade(tela, matriz, fontes_pecas):
    """ Desenha as peças (tiles) na grade. """
    y_offset = 100 # Mesma posição do fundo da grade
    for r in range(TAMANHO_GRADE):
        for c in range(TAMANHO_GRADE):
            valor = matriz[r][c]
            if valor > 0:
                x = c * (TAMANHO_PECA + MARGEM_PECA) + MARGEM_PECA
                y = r * (TAMANHO_PECA + MARGEM_PECA) + MARGEM_PECA + y_offset
                desenhar_peca(tela, valor, x, y, fontes_pecas)

def desenhar_info(tela, pontuacao, pontuacao_maxima, fonte_padrao, fonte_grande):
    """ Desenha a informação superior (Pontuação e High Score). """
    # Pontuação Atual
    texto_pontos = fonte_padrao.render("PONTOS", True, CORES['texto_claro'])
    tela.blit(texto_pontos, (MARGEM_PECA + 20, 10))
    valor_pontos = fonte_grande.render(str(pontuacao), True, CORES['texto_claro'])
    tela.blit(valor_pontos, (MARGEM_PECA + 20, 40))
    
    # Pontuação Máxima
    texto_max = fonte_padrao.render("MELHOR", True, CORES['texto_claro'])
    texto_max_rect = texto_max.get_rect(right=LARGURA - MARGEM_PECA - 20, top=10)
    tela.blit(texto_max, texto_max_rect)
    valor_max = fonte_grande.render(str(pontuacao_maxima), True, CORES['texto_claro'])
    valor_max_rect = valor_max.get_rect(right=LARGURA - MARGEM_PECA - 20, top=40)
    tela.blit(valor_max, valor_max_rect)

def desenhar_mensagem(tela, titulo, linha1, linha2, cor_fundo_rgb, fontes):
    """ Função auxiliar para desenhar sobreposições (Game Over, Vitória). """
    # Sobreposição semitransparente
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((*cor_fundo_rgb, 200)) # Alpha 200
    tela.blit(overlay, (0, 0))
    
    # Título
    titulo_surf = fontes['grande'].render(titulo, True, CORES['texto_escuro'])
    titulo_rect = titulo_surf.get_rect(center=(LARGURA // 2, ALTURA // 2 - 80))
    tela.blit(titulo_surf, titulo_rect)
    
    # Linha 1
    linha1_surf = fontes['padrao'].render(linha1, True, CORES['texto_escuro'])
    linha1_rect = linha1_surf.get_rect(center=(LARGURA // 2, ALTURA // 2))
    tela.blit(linha1_surf, linha1_rect)
    
    # Linha 2
    linha2_surf = fontes['padrao'].render(linha2, True, CORES['texto_escuro'])
    linha2_rect = linha2_surf.get_rect(center=(LARGURA // 2, ALTURA // 2 + 40))
    tela.blit(linha2_surf, linha2_rect)