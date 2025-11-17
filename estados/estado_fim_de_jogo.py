#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from src.configuracoes import *
from estados.estado_base import EstadoBase
import estados.desenho_utils as utils

# Importa o estado para o qual este pode transicionar
from estados.estado_inserir_nome import EstadoInserirNome

class EstadoFimDeJogo(EstadoBase):
    """ Gerencia a tela de Fim de Jogo (overlay). """
    def __init__(self, jogo, estado_jogo):
        super().__init__(jogo)
        self.estado_jogo = estado_jogo # Estado de jogo para desenhar no fundo

    def processar_eventos(self, evento):
        # Ao pressionar qualquer tecla, transiciona para a tela de inserir nome
        if evento.type == pygame.KEYDOWN or (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1):
            self.jogo.transicionar_para(EstadoInserirNome(self.jogo))

    def desenhar(self, tela):
        """ Desenha o jogo por baixo e a mensagem de Fim de Jogo por cima. """
        # 1. Desenha o estado de jogo (o fundo)
        self.estado_jogo.desenhar(tela)
        
        # 2. Desenha a mensagem por cima
        utils.desenhar_mensagem(tela, "Fim de Jogo!", 
                                f"Pontuação: {self.jogo.grade.pontuacao}",
                                "Pressione qualquer tecla para continuar",
                                CORES[0], # Fundo (cinza claro)
                                self.jogo.fontes_mensagem)