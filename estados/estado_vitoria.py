#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from src.configuracoes import *
from estados.estado_base import EstadoBase
import estados.desenho_utils as utils


class EstadoVitoria(EstadoBase):
    """ Gerencia a tela de Vitória (como um overlay). """
    def __init__(self, jogo, estado_jogo):
        super().__init__(jogo)
        # Armazena o estado anterior (EstadoJogando) para desenhá-lo no fundo
        self.estado_jogo = estado_jogo 

    def processar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_c: # Continuar jogando
                # Simplesmente volta ao estado de jogo
                self.jogo.transicionar_para(self.estado_jogo)
            elif evento.key == pygame.K_m: # Voltar ao menu
                from estados.estado_menu import EstadoMenu
                self.jogo.transicionar_para(EstadoMenu(self.jogo))

    def desenhar(self, tela):
        """ Desenha o jogo por baixo e a mensagem de vitória por cima. """
        # 1. Desenha o estado de jogo (o fundo)
        self.estado_jogo.desenhar(tela)
        
        # 2. Desenha a mensagem de vitória por cima
        utils.desenhar_mensagem(tela, "Você Venceu!",
                                "Pressione 'C' para continuar",
                                "ou 'M' para voltar ao Menu",
                                CORES[128], # Fundo (amarelo)
                                self.jogo.fontes_mensagem)