# 2048 - Pygame

Jogo 2048 implementado em Python 3 com Pygame.

## Requisitos

- Python 3.8 ou superior
- Pygame 2.0 ou superior

## Como Rodar

1. Instale dependências:

```bash
python3 -m pip install pygame
```

2. Execute:

```bash
python3 2048_jogo.py
```

## Controles

- **Setas (↑ ↓ ← →)**: Mover peças
- **U**: Desfazer última jogada (apenas uma vez)
- **Esc**: Sair do jogo (com confirmação)
- **No menu**: Clique em 'Novo Jogo' ou 'Ranking'

## Funcionalidades

- ✅ Grade 4x4 clássica do jogo 2048
- ✅ Sistema de pontuação com melhor pontuação (high score)
- ✅ Função desfazer (undo) uma jogada
- ✅ Detecção de vitória (ao atingir 2048)
- ✅ Detecção de game over
- ✅ Ranking persistente com top 15 pontuações
- ✅ Interface gráfica com Pygame
- ✅ Menu principal intuitivo

## Estrutura do Projeto

```
2048_v5/
├── 2048_jogo.py              # Arquivo principal
├── README.md                 # Este arquivo
├── DOCUMENTACAO.md           # Documentação técnica detalhada
├── ranking.txt               # Arquivo de ranking (gerado automaticamente)
├── src/                      # Código fonte principal
│   ├── configuracoes.py      # Constantes e configurações
│   ├── grade.py              # Lógica do jogo 2048
│   ├── botao.py              # Componente de botão
│   └── gerenciador_ranking.py # Persistência de dados
└── estados/                  # Estados da máquina de estados (FSM)
    ├── estado_base.py        # Classe base abstrata
    ├── estado_menu.py        # Menu principal
    ├── estado_jogando.py     # Tela de jogo
    ├── estado_vitoria.py     # Tela de vitória
    ├── estado_fim_de_jogo.py # Tela de game over
    ├── estado_ranking.py     # Tela de ranking
    ├── estado_inserir_nome.py # Inserção de nome
    ├── estado_confirmar_saida.py # Confirmação de saída
    └── desenho_utils.py      # Funções de desenho reutilizáveis
```

## Arquivos de Dados

O ranking é salvo automaticamente em `ranking.txt` no formato:
```
Nome | Pontuação
```

## Documentação Técnica

Para informações detalhadas sobre arquitetura, algoritmos e padrões de design utilizados, consulte [DOCUMENTACAO.md](DOCUMENTACAO.md).

## Autor

Christian Pieper  
Disciplina: Algoritmos e Estruturas de Dados I  
UniSenac
