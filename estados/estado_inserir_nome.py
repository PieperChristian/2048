#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from src.configuracoes import * # <- Importação corrigida
from estados.estado_base import EstadoBase

# Importa o estado para o qual este pode transicionar
from estados.estado_ranking import EstadoRanking

class EstadoInserirNome(EstadoBase):
    """ Gerencia a tela de inserção de nome. """
    def __init__(self, jogo):
        super().__init__(jogo)
        self.nome_jogador = ""

    def processar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN: # Enter
                if self.nome_jogador:
                    # --- LÓGICA ATUALIZADA ---
                    # 1. Delega a ação para o gerenciador de ranking
                    self.jogo.gerenciador_ranking.salvar_pontuacao(self.nome_jogador, self.jogo.grade.pontuacao)
                    # 2. Atualiza a pontuação máxima na classe Jogo
                    self.jogo.pontuacao_maxima = self.jogo.gerenciador_ranking.carregar_pontuacao_maxima()
                    # -------------------------
                    
                    # Vai para a tela de ranking
                    self.jogo.transicionar_para(EstadoRanking(self.jogo))
            elif evento.key == pygame.K_BACKSPACE:
                self.nome_jogador = self.nome_jogador[:-1]
            elif evento.key != pygame.K_ESCAPE and evento.key != pygame.K_RETURN:
                if len(self.nome_jogador) < 20 and evento.unicode.isprintable():
                    self.nome_jogador += evento.unicode

    def desenhar(self, tela):
        """ Desenha a tela para inserir o nome do jogador. """
        tela.fill(CORES['fundo'])
        titulo = self.jogo.fonte_grande.render("Fim de Jogo", True, CORES['texto_escuro'])
        titulo_rect = titulo.get_rect(center=(LARGURA // 2, ALTURA // 4))
        tela.blit(titulo, titulo_rect)

        pontos_str = f"Sua pontuação: {self.jogo.grade.pontuacao}"
        pontos_surf = self.jogo.fonte_padrao.render(pontos_str, True, CORES['texto_escuro'])
        pontos_rect = pontos_surf.get_rect(center=(LARGURA // 2, ALTURA // 2 - 60))
        tela.blit(pontos_surf, pontos_rect)
        
        prompt = self.jogo.fonte_padrao.render("Digite seu nome:", True, CORES['texto_escuro'])
        prompt_rect = prompt.get_rect(center=(LARGURA // 2, ALTURA // 2))
        tela.blit(prompt, prompt_rect)
        
        # Caixa de texto
        caixa_rect = pygame.Rect(LARGURA // 4, ALTURA // 2 + 40, LARGURA // 2, 50)
        pygame.draw.rect(tela, CORES[0], caixa_rect, border_radius=5)
        
        # Texto do nome (com cursor piscando)
        nome_com_cursor = self.nome_jogador
        if int(pygame.time.get_ticks() / 500) % 2 == 0:
            nome_com_cursor += "_"
            
        nome_surf = self.jogo.fonte_padrao.render(nome_com_cursor, True, CORES['texto_escuro'])
        nome_rect = nome_surf.get_rect(center=caixa_rect.center)
        tela.blit(nome_surf, nome_rect)
        
        hint = self.jogo.fonte_padrao.render("Pressione ENTER para salvar", True, CORES['texto_escuro'])
        hint_rect = hint.get_rect(center=(LARGURA // 2, ALTURA - 40))
        tela.blit(hint, hint_rect)