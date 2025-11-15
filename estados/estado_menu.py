#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from src.configuracoes import *
from src.botao import Botao
from src.grade import Grade
from estados.estado_base import EstadoBase

class EstadoMenu(EstadoBase):
    """ Gerencia o Menu Principal. """
    def __init__(self, jogo):
        super().__init__(jogo)
        
        # Cria os botões do menu
        largura_btn = LARGURA // 2
        altura_btn = 60
        x_btn = LARGURA // 4
        self.btn_novo_jogo = Botao(x_btn, ALTURA // 2 - 50, largura_btn, altura_btn, 
                                    "Novo Jogo", CORES[8], CORES['texto_claro'])
        self.btn_ranking = Botao(x_btn, ALTURA // 2 + 30, largura_btn, altura_btn, 
                                    "Ranking", CORES[16], CORES['texto_claro'])

    def processar_eventos(self, evento):
        if self.btn_novo_jogo.foi_clicado(evento):
            # Cria uma nova grade e transiciona para o estado de jogo
            self.jogo.grade = Grade(TAMANHO_GRADE)
            self.jogo.venceu = False
            from estados.estado_jogando import EstadoJogando
            self.jogo.transicionar_para(EstadoJogando(self.jogo))
            
        elif self.btn_ranking.foi_clicado(evento):
            from estados.estado_ranking import EstadoRanking
            self.jogo.transicionar_para(EstadoRanking(self.jogo))
            
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            # Transiciona para o estado de confirmação, passando este estado (self)
            # como o estado para o qual deve voltar se o usuário cancelar.
            from estados.estado_confirmar_saida import EstadoConfirmarSaida
            self.jogo.transicionar_para(EstadoConfirmarSaida(self.jogo, self))

    def desenhar(self, tela):
        """ Desenha a tela do menu principal. """
        tela.fill(CORES['fundo'])
        titulo = self.jogo.fonte_grande.render("2048", True, CORES['texto_escuro'])
        titulo_rect = titulo.get_rect(center=(LARGURA // 2, ALTURA // 4))
        tela.blit(titulo, titulo_rect)
        
        self.btn_novo_jogo.desenhar(tela, self.jogo.fonte_padrao)
        self.btn_ranking.desenhar(tela, self.jogo.fonte_padrao)