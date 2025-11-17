#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Classe abstrata base para o padrão State (FSM)."""

class EstadoBase:
    """Classe base abstrata para todos os estados do jogo (State Pattern)."""
    def __init__(self, jogo):
        """Inicializa estado com referência ao jogo principal."""
        self.jogo = jogo # Referência à classe Jogo principal

    def processar_eventos(self, evento):
        """Processa evento do Pygame (abstrato - sobrescrever nas subclasses)."""
        pass

    def desenhar(self, tela):
        """Desenha o estado na tela (abstrato - sobrescrever nas subclasses)."""
        pass