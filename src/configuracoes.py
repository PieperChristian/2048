#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Configurações globais do jogo: dimensões, FPS, cores e constantes."""

# --- Configurações da Grade e Tela ---
TAMANHO_GRADE = 4
TAMANHO_PECA = 100
MARGEM_PECA = 16

# Largura da tela (calculada)
LARGURA = TAMANHO_GRADE * TAMANHO_PECA + (TAMANHO_GRADE + 1) * MARGEM_PECA
# Altura da tela (com espaço para HUD superior e inferior)
ALTURA = LARGURA + 180

# --- Configurações do Jogo ---
FPS = 60
ARQUIVO_RANKING = "ranking.txt"

# --- Dicionário de Cores (RGB) ---
CORES = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    'fundo': (187, 173, 160),
    'texto_escuro': (119, 110, 101),
    'texto_claro': (249, 246, 242)
}