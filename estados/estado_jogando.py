#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from src.configuracoes import *
from estados.estado_base import EstadoBase
import estados.desenho_utils as utils # Importa as funções de desenho

class EstadoJogando(EstadoBase):
    """ Gerencia a tela principal do jogo. """
    def __init__(self, jogo):
        super().__init__(jogo)
        self.moveu = False # Controla se o último movimento foi válido

    def _processar_movimento(self, direcao):
        """ Processa um movimento do jogador e suas consequências. """
        self.jogo.grade.salvar_estado_desfazer() # Salva o estado *antes* de mover
        
        if direcao == 'esquerda':
            self.moveu = self.jogo.grade.mover_esquerda()
        elif direcao == 'direita':
            self.moveu = self.jogo.grade.mover_direita()
        elif direcao == 'cima':
            self.moveu = self.jogo.grade.mover_cima()
        elif direcao == 'baixo':
            self.moveu = self.jogo.grade.mover_baixo()

        if self.moveu:
            self.jogo.grade.gerar_nova_peca()
            if self.jogo.grade.pontuacao > self.jogo.pontuacao_maxima:
                self.jogo.pontuacao_maxima = self.jogo.grade.pontuacao
            
            # Verifica Vitória (só na primeira vez)
            if self.jogo.grade.maior_peca() == 2048 and not self.jogo.venceu:
                self.jogo.venceu = True
                from estados.estado_vitoria import EstadoVitoria
                self.jogo.transicionar_para(EstadoVitoria(self.jogo, self)) # Passa o estado atual
            # Verifica Fim de Jogo
            elif not self.jogo.grade.pode_mover():
                from estados.estado_fim_de_jogo import EstadoFimDeJogo
                self.jogo.transicionar_para(EstadoFimDeJogo(self.jogo, self)) # Passa o estado atual
        else:
            # Se não moveu, invalida o 'desfazer'
            self.jogo.grade.pode_desfazer = False

    def processar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                from estados.estado_confirmar_saida import EstadoConfirmarSaida
                self.jogo.transicionar_para(EstadoConfirmarSaida(self.jogo, self))
            elif evento.key == pygame.K_LEFT:
                self._processar_movimento('esquerda')
            elif evento.key == pygame.K_RIGHT:
                self._processar_movimento('direita')
            elif evento.key == pygame.K_UP:
                self._processar_movimento('cima')
            elif evento.key == pygame.K_DOWN:
                self._processar_movimento('baixo')
            elif evento.key == pygame.K_u: # Tecla 'U' para Desfazer
                self.jogo.grade.carregar_estado_desfazer()

    def desenhar(self, tela):
        """ Desenha a tela de jogo. """
        utils.desenhar_fundo(tela)
        utils.desenhar_grade(tela, self.jogo.grade.matriz, self.jogo.fontes_pecas)
        utils.desenhar_info(tela, self.jogo.grade.pontuacao, self.jogo.pontuacao_maxima, 
                            self.jogo.fonte_padrao, self.jogo.fonte_grande)
        
        # Dica
        hint = self.jogo.fonte_pequena.render("Use as setas. 'U' para desfazer. 'Esc' para sair.", True, CORES['texto_escuro'])
        hint_rect = hint.get_rect(center=(LARGURA // 2, ALTURA - 30))
        tela.blit(hint, hint_rect)