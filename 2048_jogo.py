#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Arquivo Principal do Jogo 2048 em Pygame

Implementa o jogo 2048 usando Pygame e o padrão State Machine (FSM).
A classe Jogo gerencia o loop principal, estados e recursos compartilhados.

Autor: Christian Pieper
Disciplina: Algoritmos e Estruturas de Dados I - UniSenac
"""

import pygame
import os
import sys

# Importa as classes e constantes do NOVO pacote 'core'
from src.configuracoes import *
from src.grade import Grade
from src.botao import Botao
from src.gerenciador_ranking import GerenciadorRanking

# Importa o PRIMEIRO estado
from estados.estado_menu import EstadoMenu

class Jogo:
    """
    Gerenciador Principal do Jogo 2048.
    
    Controla o loop principal, estados da FSM e recursos compartilhados.
    """
    
    def __init__(self):
        """Inicializa o jogo, configurando Pygame, fontes e estado inicial."""
        pygame.init()
        pygame.font.init()
        
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Jogo 2048")
        self.relogio = pygame.time.Clock()

        # --- Fontes Globais ---
        try:
            self.fonte_padrao = pygame.font.SysFont("Arial", 30)
            self.fonte_grande = pygame.font.SysFont("Arial", 50, bold=True)
            self.fonte_pequena = pygame.font.SysFont("Arial", 18)
            self.fonte_ranking = pygame.font.SysFont("Consolas", 24)
            self.fontes_pecas = {
                1: pygame.font.SysFont("Arial", 55, bold=True),
                2: pygame.font.SysFont("Arial", 55, bold=True),
                3: pygame.font.SysFont("Arial", 45, bold=True),
                4: pygame.font.SysFont("Arial", 35, bold=True),
            }
        except Exception as e:
            print(f"Erro ao carregar fontes. Usando fontes padrão: {e}")
            self.fonte_padrao = pygame.font.Font(None, 30)
            self.fonte_grande = pygame.font.Font(None, 50)
            self.fonte_pequena = pygame.font.Font(None, 18)
            self.fonte_ranking = pygame.font.Font(None, 24)
            self.fontes_pecas = {
                1: pygame.font.Font(None, 55), 2: pygame.font.Font(None, 55),
                3: pygame.font.Font(None, 45), 4: pygame.font.Font(None, 35),
            }
        self.fontes_mensagem = {'padrao': self.fonte_padrao, 'grande': self.fonte_grande}

        # --- Gerenciamento de Dados ---
        # A classe Jogo AGORA DELEGA a responsabilidade de I/O de arquivo
        # para uma classe especialista.
        self.gerenciador_ranking = GerenciadorRanking(ARQUIVO_RANKING)

        # --- Dados Globais do Jogo ---
        self.pontuacao_maxima = self.gerenciador_ranking.carregar_pontuacao_maxima()
        self.grade = None # Será criada pelo EstadoMenu/EstadoJogando
        self.venceu = False # Controla a mensagem de vitória
        self.executando = True

        # --- Sistema de Estados ---
        self.estado_atual = EstadoMenu(self)

    def transicionar_para(self, novo_estado):
        """Realiza transição para um novo estado da FSM."""
        self.estado_atual = novo_estado

    def executar(self):
        """Loop principal do jogo."""
        while self.executando:
            self.relogio.tick(FPS)
            
            # Processa eventos, desenha na tela e atualiza
            self.processar_eventos()
            self.desenhar()
            
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()

    def processar_eventos(self):
        """Processa eventos do Pygame e delega para o estado atual."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.executando = False
                return

            # Repassa o evento para o estado atual tratá-lo
            self.estado_atual.processar_eventos(evento)

    def desenhar(self):
        """Limpa a tela e delega o desenho para o estado atual."""
        self.tela.fill(CORES['fundo']) # Limpa a tela
        self.estado_atual.desenhar(self.tela)

# --- Função Principal ---
def principal():
    """Função principal que inicializa e executa o jogo."""
    jogo = Jogo()
    jogo.executar()


if __name__ == "__main__":
    principal()