#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from src.configuracoes import *
from estados.estado_base import EstadoBase

class EstadoRanking(EstadoBase):
    """ Gerencia a tela de Ranking. """
    def __init__(self, jogo):
        super().__init__(jogo)
        # Carrega os dados do ranking assim que o estado é criado
        self.linhas_ranking = self.jogo.gerenciador_ranking.ler_ranking()

    def processar_eventos(self, evento):
        # Volta ao menu com qualquer tecla ou clique
        if evento.type == pygame.KEYDOWN or (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1):
            from estados.estado_menu import EstadoMenu
            self.jogo.transicionar_para(EstadoMenu(self.jogo))

    def desenhar(self, tela):
        """ Desenha a tela de ranking. """
        tela.fill(CORES['fundo'])
        titulo = self.jogo.fonte_grande.render("Ranking", True, CORES['texto_escuro'])
        titulo_rect = titulo.get_rect(center=(LARGURA // 2, 60))
        tela.blit(titulo, titulo_rect)

        y_pos = 120
        for linha in self.linhas_ranking:
            linha_surf = self.jogo.fonte_ranking.render(linha, True, CORES['texto_escuro'])
            linha_rect = linha_surf.get_rect(center=(LARGURA // 2, y_pos))
            tela.blit(linha_surf, linha_rect)
            y_pos += 30
            
        hint = self.jogo.fonte_padrao.render("Pressione qualquer tecla para voltar", True, CORES['texto_escuro'])
        hint_rect = hint.get_rect(center=(LARGURA // 2, ALTURA - 40))
        tela.blit(hint, hint_rect)