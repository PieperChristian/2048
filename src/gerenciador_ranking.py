#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Gerencia persistência de dados do ranking (leitura/escrita em arquivo)."""

import os

class GerenciadorRanking:
    """Gerencia persistência do ranking em arquivo (formato: Nome|Pontuação)."""
    def __init__(self, arquivo_ranking):
        """Inicializa gerenciador com o caminho do arquivo de ranking."""
        self.arquivo_ranking = arquivo_ranking

    def carregar_pontuacao_maxima(self):
        """Retorna a maior pontuação de todo o histórico (0 se vazio)."""
        if not os.path.isfile(self.arquivo_ranking):
            return 0
        try:
            with open(self.arquivo_ranking, "r") as arq:
                dados = arq.readlines()
                if not dados: return 0
                pontuacoes = []
                for linha in dados:
                    partes = linha.strip().split('|')
                    if len(partes) > 1:
                        pontuacoes.append(int(partes[1].strip()))
                    elif partes[0]:
                        pontuacoes.append(int(partes[0].strip()))
                return max(pontuacoes) if pontuacoes else 0
        except Exception as e:
            print(f"Erro ao ler ranking (carregar_pontuacao_maxima): {e}")
            return 0

    def salvar_pontuacao(self, nome, pontuacao):
        """Salva nome e pontuação no arquivo (formato: Nome | Pontuação)."""
        try:
            with open(self.arquivo_ranking, "a") as arq:
                arq.write(f"{nome} | {pontuacao}\n")
        except Exception as e:
            print(f"Erro ao salvar pontuação: {e}")

    def ler_ranking(self):
        """Retorna lista formatada com top 15 pontuações (ordenadas decrescente)."""
        if not os.path.isfile(self.arquivo_ranking):
            return ["Ranking vazio."]
        dados = []
        try:
            with open(self.arquivo_ranking, "r") as arq:
                linhas = arq.readlines()
                for linha in linhas:
                    partes = linha.strip().split('|')
                    if len(partes) > 1:
                        nome = partes[0].strip()
                        pontuacao = int(partes[1].strip())
                        dados.append((nome, pontuacao))
                    elif partes[0]:
                        nome = "Jogador"
                        pontuacao = int(partes[0].strip())
                        dados.append((nome, pontuacao))
            
            dados.sort(key=lambda item: item[1], reverse=True)
            dados_formatados = []
            for i, (nome, pontuacao) in enumerate(dados[:15]): # Limita aos 15 melhores
                dados_formatados.append(f"{i+1: >2}. {nome: <20} {pontuacao: >8}")
            
            return dados_formatados if dados_formatados else ["Ranking vazio."]
        except Exception as e:
            print(f"Erro ao ler ranking: {e}")
            return ["Erro ao ler ranking."]