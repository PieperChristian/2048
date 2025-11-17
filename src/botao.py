#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Implementa um botão clicável reutilizável com efeito hover."""

import pygame

class Botao:
    """Botão clicável com efeito hover."""
    def __init__(self, x, y, largura, altura, texto, cor_fundo, cor_texto):
        """Inicializa botão com posição, dimensões, texto e cores."""
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_fundo = cor_fundo
        self.cor_texto = cor_texto
        # Escurece a cor para o efeito 'hover'
        self.cor_fundo_hover = (max(0, cor_fundo[0] - 30), 
                                max(0, cor_fundo[1] - 30), 
                                max(0, cor_fundo[2] - 30))

    def desenhar(self, tela, fonte):
        """Desenha o botão na tela com efeito hover."""
        mouse_pos = pygame.mouse.get_pos()
        cor_atual = self.cor_fundo_hover if self.rect.collidepoint(mouse_pos) else self.cor_fundo
        
        pygame.draw.rect(tela, cor_atual, self.rect, border_radius=10)
        
        texto_surf = fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        tela.blit(texto_surf, texto_rect)

    def foi_clicado(self, evento):
        """Verifica se o botão foi clicado (botão esquerdo do mouse)."""
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1 and self.rect.collidepoint(evento.pos):
                return True
        return False