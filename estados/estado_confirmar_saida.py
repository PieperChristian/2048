#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from src.configuracoes import *
from estados.estado_base import EstadoBase
import estados.desenho_utils as utils

class EstadoConfirmarSaida(EstadoBase):
    """ Gerencia a tela de confirmação de saída (overlay). """
    def __init__(self, jogo, estado_anterior):
        super().__init__(jogo)
        # Armazena o estado anterior para saber para onde voltar
        self.estado_anterior = estado_anterior 

    def processar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_s: # 'S' para Sim
                self.jogo.executando = False # Encerra o jogo
            elif evento.key == pygame.K_n or evento.key == pygame.K_ESCAPE: # 'N' ou Esc para Não
                # Volta ao estado anterior
                self.jogo.transicionar_para(self.estado_anterior)

    def desenhar(self, tela):
        """ Desenha o estado anterior por baixo e a mensagem por cima. """
        # 1. Desenha o estado anterior (Menu ou Jogo)
        self.estado_anterior.desenhar(tela)
        
        # 2. Desenha a mensagem de confirmação por cima
        utils.desenhar_mensagem(tela, "Sair do Jogo",
                                "Tem certeza que deseja sair?",
                                "Pressione [S] para Sim ou [N] para Não",
                                CORES['fundo'],
                                self.jogo.fontes_mensagem)