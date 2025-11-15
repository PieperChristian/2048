# Documentação Técnica - Jogo 2048

**Autor:** Christian Pieper  
**Disciplina:** Algoritmos e Estruturas de Dados I - UniSenac  
**Versão:** 1.0  
**Data:** Novembro de 2025

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Estrutura de Diretórios](#estrutura-de-diretórios)
4. [Padrões de Design Utilizados](#padrões-de-design-utilizados)
5. [Módulos e Classes](#módulos-e-classes)
6. [Detalhamento de Métodos](#detalhamento-de-métodos)
7. [Algoritmos Principais](#algoritmos-principais)
8. [Fluxo de Estados](#fluxo-de-estados)
9. [Estruturas de Dados](#estruturas-de-dados)
10. [Como Executar](#como-executar)
11. [Como Estender](#como-estender)

---

## Visão Geral

Este projeto implementa o jogo 2048 utilizando Python e Pygame, seguindo princípios de Programação Orientada a Objetos e padrões de design modernos.

### Características Principais

- **Arquitetura FSM (Finite State Machine)**: Cada tela é um estado independente
- **Código Modular**: Separação clara de responsabilidades
- **Documentação Extensiva**: Docstrings detalhadas em todo o código
- **Persistência de Dados**: Sistema de ranking com arquivo
- **Interface Gráfica**: Botões interativos com efeito hover
- **Sistema de Undo**: Possibilidade de desfazer último movimento

---

## Arquitetura do Sistema

### Diagrama de Componentes

```
┌─────────────────────────────────────────┐
│        2048_jogo.py (Main)              │
│  ┌───────────────────────────────────┐  │
│  │    Classe Jogo (Game Manager)    │  │
│  │  - Loop principal                │  │
│  │  - Gerenciamento de estados      │  │
│  │  - Recursos compartilhados        │  │
│  └───────────────┬───────────────────┘  │
└──────────────────┼──────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
┌───────▼──────┐ ┌─▼────────┐ ┌▼──────────────┐
│  src/        │ │ estados/ │ │ ranking.txt   │
│              │ │          │ │               │
│ - Grade      │ │ - Menu   │ │ Persistência  │
│ - Botao      │ │ - Jogando│ │               │
│ - Config     │ │ - Vitoria│ └───────────────┘
│ - Ranking    │ │ - GameOvr│
└──────────────┘ └──────────┘
```

### Camadas da Aplicação

1. **Camada de Apresentação** (`estados/`)
   - Gerencia interface e interação com usuário
   - Cada estado é independente e focado

2. **Camada de Lógica** (`src/`)
   - Implementa regras do jogo
   - Gerencia estruturas de dados

3. **Camada de Persistência** (`GerenciadorRanking`)
   - Leitura/escrita de arquivos
   - Formatação de dados

---

## Estrutura de Diretórios

```
2048_v5/
├── 2048_jogo.py              # Arquivo principal (entry point)
├── ranking.txt               # Persistência do ranking
├── README.md                 # Documentação básica
├── DOCUMENTACAO.md          # Esta documentação técnica
├── src/                     # Módulo core do jogo
│   ├── __init__.py
│   ├── configuracoes.py     # Constantes globais
│   ├── grade.py             # Lógica do tabuleiro
│   ├── botao.py             # Componente de UI
│   └── gerenciador_ranking.py  # Persistência
└── estados/                 # Estados da FSM
    ├── __init__.py
    ├── estado_base.py       # Classe abstrata
    ├── estado_menu.py       # Tela inicial
    ├── estado_jogando.py    # Jogo principal
    ├── estado_vitoria.py    # Overlay de vitória
    ├── estado_fim_de_jogo.py  # Overlay game over
    ├── estado_inserir_nome.py  # Entrada de nome
    ├── estado_ranking.py    # Exibição do ranking
    ├── estado_confirmar_saida.py  # Confirmação de saída
    └── desenho_utils.py     # Funções de desenho reutilizáveis
```

---

## Padrões de Design Utilizados

### 1. State Pattern (Padrão Estado)

**Problema Resolvido:** Gerenciar diferentes telas sem condicionais complexos

**Implementação:**
```python
class EstadoBase:  # Interface comum
    def processar_eventos(self, evento): pass
    def desenhar(self, tela): pass

class EstadoMenu(EstadoBase):  # Estado concreto
    def processar_eventos(self, evento):
        # Lógica específica do menu
    def desenhar(self, tela):
        # Desenho específico do menu
```

**Benefícios:**
- Eliminação de if/elif gigantes
- Cada estado encapsula seu comportamento
- Fácil adicionar novos estados

### 2. Repository Pattern (Padrão Repositório)

**Problema Resolvido:** Abstrair detalhes de persistência de dados

**Implementação:**
```python
class GerenciadorRanking:
    def carregar_pontuacao_maxima(self): ...
    def salvar_pontuacao(self, nome, pontuacao): ...
    def ler_ranking(self): ...
```

**Benefícios:**
- Separação de responsabilidades
- Facilita mudanças no formato de armazenamento
- Testável (pode mockar)

### 3. Single Responsibility Principle (SRP)

**Aplicação:** Cada classe tem uma única responsabilidade

- `Grade`: Lógica do jogo 2048
- `Botao`: Componente de UI
- `GerenciadorRanking`: Persistência
- Cada estado: Comportamento de uma tela específica

### 4. DRY (Don't Repeat Yourself)

**Implementação:** Módulo `desenho_utils.py`

Funções reutilizáveis evitam duplicação:
```python
desenhar_fundo(tela)
desenhar_grade(tela, matriz, fontes)
desenhar_mensagem(tela, titulo, ...)
```

---

## Módulos e Classes

### 2048_jogo.py

#### Classe `Jogo`

**Responsabilidades:**
- Gerenciar loop principal do jogo
- Coordenar transições entre estados
- Manter recursos compartilhados (fontes, tela, pontuação máxima)

**Atributos Principais:**
```python
tela: pygame.Surface           # Janela do jogo
estado_atual: EstadoBase      # Estado FSM atual
grade: Grade                  # Tabuleiro 4x4
pontuacao_maxima: int        # Melhor pontuação histórica
gerenciador_ranking: GerenciadorRanking  # Persistência
executando: bool             # Controle do loop
```

**Métodos Principais:**
```python
executar()                   # Loop principal
processar_eventos()          # Delega eventos ao estado
desenhar()                   # Delega desenho ao estado
transicionar_para(estado)    # Muda estado atual
```

### src/grade.py

#### Classe `Grade`

**Responsabilidades:**
- Gerenciar matriz 4x4 do jogo
- Implementar lógica de movimento e fusão
- Calcular pontuação
- Sistema de desfazer (undo)

**Algoritmo Central: `_mover_linha_esquerda(linha)`**

```python
def _mover_linha_esquerda(self, linha):
    # ETAPA 1: Compressão
    # Remove zeros: [2, 0, 2, 4] → [2, 2, 4]
    nova_linha = [i for i in linha if i != 0]
    
    # ETAPA 2: Fusão
    # Combina adjacentes iguais: [2, 2, 4] → [4, 4]
    i = 0
    while i < len(nova_linha) - 1:
        if nova_linha[i] == nova_linha[i+1]:
            nova_linha[i] *= 2
            pontos_ganhos += nova_linha[i]
            nova_linha.pop(i+1)
        i += 1
    
    # ETAPA 3: Preenchimento
    # Completa com zeros: [4, 4] → [4, 4, 0, 0]
    while len(nova_linha) < self.tamanho:
        nova_linha.append(0)
    
    return nova_linha, pontos_ganhos
```

**Reutilização para Todas as Direções:**

| Direção   | Transformação                                           |
|-----------|---------------------------------------------------------|
| Esquerda  | Direto                                                  |
| Direita   | Inverter → Esquerda → Desinverter                       |
| Cima      | Transpor → Esquerda → Transpor                          |
| Baixo     | Transpor → Inverter → Esquerda → Desinverter → Transpor |

**Complexidade:**
- Movimento: O(n²) onde n = tamanho da grade
- Verificação game over: O(n²)
- Espaço: O(n²) para matriz

### src/botao.py

#### Classe `Botao`

**Responsabilidades:**
- Renderizar botão clicável
- Detectar cliques
- Efeito hover (mudança de cor)

**Cálculo de Cor Hover:**
```python
# Escurece cada componente RGB em 30
cor_hover = (max(0, R-30), max(0, G-30), max(0, B-30))
```

### src/gerenciador_ranking.py

#### Classe `GerenciadorRanking`

**Responsabilidades:**
- Ler/escrever arquivo ranking.txt
- Ordenar e formatar dados
- Calcular pontuação máxima

**Formato do Arquivo:**
```
Nome|Pontuação
Christian|2184
Pieper|2352
```

**Algoritmo de Leitura:**
```python
1. Lê todas as linhas
2. Parse: separa por '|'
3. Ordena por pontuação (decrescente)
4. Limita aos 15 melhores
5. Formata para exibição
```

### estados/estado_base.py

#### Classe `EstadoBase` (Abstrata)

**Interface comum para todos os estados:**
```python
class EstadoBase:
    def __init__(self, jogo):
        self.jogo = jogo
    
    def processar_eventos(self, evento):
        pass  # Implementado pelas subclasses
    
    def desenhar(self, tela):
        pass  # Implementado pelas subclasses
```

### Estados Concretos

| Estado               | Responsabilidade                    | Transições Possíveis              |
|----------------------|-------------------------------------|----------------------------------|
| EstadoMenu          | Tela inicial                        | → Jogando, Ranking, ConfirmarSaída |
| EstadoJogando       | Jogo principal                      | → Vitória, GameOver, ConfirmarSaída |
| EstadoVitoria       | Overlay ao atingir 2048            | → Jogando (continuar), Menu       |
| EstadoFimDeJogo     | Overlay quando não há movimentos   | → InserirNome                     |
| EstadoInserirNome   | Captura nome do jogador            | → Ranking                         |
| EstadoRanking       | Exibe top 15 pontuações            | → Menu                            |
| EstadoConfirmarSaida| Confirmação antes de sair          | → Estado anterior, ou Encerrar    |

---

## Detalhamento de Métodos

### Classe Jogo (2048_jogo.py)

#### `__init__(self)`

**Propósito:** Inicializa o jogo e todos os recursos necessários.

**Processo:**
1. Inicializa módulos do Pygame (pygame.init, pygame.font.init)
2. Cria a janela do jogo (480x660 pixels)
3. Carrega fontes (Arial em vários tamanhos)
4. Inicializa gerenciador de ranking
5. Carrega pontuação máxima do histórico
6. Define EstadoMenu como estado inicial

**Tratamento de Erros:** Se falhar ao carregar fontes do sistema, usa fontes padrão do Pygame como fallback.

---

#### `transicionar_para(self, novo_estado)`

**Propósito:** Realiza transição entre estados da FSM.

**Parâmetros:**
- `novo_estado`: Instância de EstadoBase (ou subclasse)

**Exemplos de Transições:**
- `EstadoMenu → EstadoJogando`: Usuário clica "Novo Jogo"
- `EstadoJogando → EstadoVitoria`: Atinge peça 2048
- `EstadoJogando → EstadoFimDeJogo`: Sem movimentos possíveis

**Implementação:** Simplesmente substitui `self.estado_atual` pelo novo estado.

---

#### `executar(self)`

**Propósito:** Loop principal do jogo (Game Loop clássico).

**Estrutura do Loop:**
1. Controla FPS (60 por segundo via `self.relogio.tick(FPS)`)
2. Processa eventos (`processar_eventos()`)
3. Desenha estado atual (`desenhar()`)
4. Atualiza display (`pygame.display.flip()`)

**Encerramento:** Quando `self.executando = False`, chama `pygame.quit()` e `sys.exit()`.

---

#### `processar_eventos(self)`

**Propósito:** Captura eventos do Pygame e delega ao estado atual.

**Eventos Tratados:**
1. `pygame.QUIT`: Define `self.executando = False` (encerra jogo)
2. Outros eventos: Delegados para `estado_atual.processar_eventos(evento)`

**Padrão de Delegação:** A classe Jogo não precisa conhecer detalhes de cada estado, mantendo código desacoplado.

---

#### `desenhar(self)`

**Propósito:** Limpa a tela e delega desenho ao estado atual.

**Processo:**
1. Preenche tela com cor de fundo (limpa frame anterior)
2. Chama `estado_atual.desenhar(self.tela)`
3. Display é atualizado no `executar()` via `pygame.display.flip()`

---

### Classe Grade (src/grade.py)

#### `__init__(self, tamanho)`

**Propósito:** Inicializa nova grade de jogo.

**Parâmetros:**
- `tamanho`: Dimensão da grade (padrão: 4 para 4x4)

**Inicialização:**
1. Cria matriz zerada: `[[0] * tamanho for _ in range(tamanho)]`
2. Zera pontuação
3. Inicializa sistema de desfazer
4. Gera duas peças iniciais (2 ou 4)

**Por que list comprehension?** Garante que cada linha seja lista independente.

---

#### `salvar_estado_desfazer(self)`

**Propósito:** Salva estado atual antes de movimento.

**Por que `copy.deepcopy`?**
A matriz é lista de listas. Cópia simples (shallow) copiaria apenas referências:
```python
# ERRADO (shallow copy)
backup = self.matriz  # Apenas copia referência!
self.matriz[0][0] = 4  # Modifica backup também!

# CORRETO (deep copy)
backup = copy.deepcopy(self.matriz)
self.matriz[0][0] = 4  # backup permanece inalterado
```

**Resultado:** Define `pode_desfazer = True`, permitindo uso de 'U'.

---

#### `carregar_estado_desfazer(self)`

**Propósito:** Restaura estado salvo (undo).

**Funcionamento:**
1. Verifica se `pode_desfazer == True`
2. Se sim, restaura matriz e pontuação
3. Define `pode_desfazer = False` (só pode desfazer UMA vez)

**Fluxo de Uso:**
1. Jogador move (estado salvo, `pode_desfazer = True`)
2. Pressiona 'U' (estado restaurado, `pode_desfazer = False`)
3. Pressiona 'U' novamente (nada acontece)

---

#### `gerar_nova_peca(self)`

**Propósito:** Gera peça (2 ou 4) em célula vazia aleatória.

**Algoritmo:**
1. Varre matriz procurando células com valor 0
2. Armazena coordenadas `(r, c)` de todas vazias
3. Escolhe aleatoriamente uma posição
4. Gera valor: 90% chance de 2, 10% chance de 4 (como jogo original)

**Complexidade:**
- Tempo: O(n²) onde n = tamanho da grade
- Espaço: O(k) onde k = número de células vazias

**Caso Especial:** Se não houver vazias, nada acontece (não deveria ocorrer em jogo normal).

---

#### `pode_mover(self)`

**Propósito:** Verifica se há movimentos possíveis (detecta Game Over).

**Algoritmo (duas etapas):**

**Etapa 1 - Verifica células vazias:**
- Se encontrar qualquer 0, retorna True imediatamente
- Movimento possível porque peças podem deslizar

**Etapa 2 - Verifica fusões adjacentes:**
- Para cada célula, verifica:
  - Célula à direita (horizontal)
  - Célula abaixo (vertical)
- Se valores forem iguais, retorna True

**Otimização:** Usa short-circuit evaluation (retorna True assim que encontra possibilidade).

**Complexidade:**
- Melhor caso: O(1) - encontra vazia na primeira posição
- Pior caso: O(n²) - varre toda matriz

**Exemplo de Game Over:**
```python
[[2, 4, 2, 4],
 [4, 2, 4, 2],
 [2, 4, 2, 4],
 [4, 2, 4, 2]]
# Sem vazias, sem adjacentes iguais → Game Over
```

---

#### `_mover_linha_esquerda(self, linha)`

**Propósito:** Algoritmo CORE do jogo - move e funde uma linha.

**Retorno:** `(nova_linha, pontos_ganhos)`

**Regra Importante:** Cada peça só pode fundir UMA vez por movimento.
Exemplo: `[2, 2, 4] → [4, 4]`, NÃO `[8]`

**Exemplos Completos:**
```python
[2, 2, 2, 2] → [4, 4, 0, 0] (+8 pontos)
[0, 2, 0, 2] → [4, 0, 0, 0] (+4 pontos)
[2, 4, 8, 16] → [2, 4, 8, 16] (+0 pontos)
[4, 4, 2, 2] → [8, 4, 0, 0] (+12 pontos)
```

**Complexidade:**
- Tempo: O(n)
- Espaço: O(n) para nova_linha

---

#### `mover_esquerda(self)`, `mover_direita(self)`, `mover_cima(self)`, `mover_baixo(self)`

**Propósito:** Executa movimento em direção específica.

**Retorno:** `True` se movimento alterou matriz, `False` caso contrário.

**Estratégias de Reutilização:**

| Método          | Transformação                                           |
|-----------------|---------------------------------------------------------|
| mover_esquerda  | Direto: aplica `_mover_linha_esquerda`                 |
| mover_direita   | Inverte → move esquerda → desinverte                    |
| mover_cima      | Transpõe → move esquerda → transpõe                     |
| mover_baixo     | Transpõe → inverte → move esquerda → desinverte → transpõe |

**Exemplo Visual (mover_direita):**
```python
Original:       [0, 2, 0, 2]
Inverte:        [2, 0, 2, 0]
Move esquerda:  [4, 0, 0, 0]
Desinverte:     [0, 0, 0, 4]  ✓ Correto!
```

**Transposição em Python:**
```python
# zip(*matriz) é idioma Python para transpor
matriz = [[1,2],[3,4]]
transposta = [list(col) for col in zip(*matriz)]
# Resultado: [[1,3],[2,4]]
```

---

#### `maior_peca(self)`

**Propósito:** Retorna valor da maior peça na matriz.

**Utilidade:**
- Verificar condição de vitória (>= 2048)
- Estatísticas do jogo
- Determinar progresso

**Complexidade:** O(n²)

**Exemplos:**
```python
grade.matriz = [[2,4],[8,16]]
grade.maior_peca()  # Retorna 16

grade.matriz = [[0,0],[0,2048]]
grade.maior_peca()  # Retorna 2048 (Vitória!)
```

---

### Classe Botao (src/botao.py)

#### `__init__(self, x, y, largura, altura, texto, cor_fundo, cor_texto)`

**Propósito:** Inicializa botão clicável com efeito hover.

**Parâmetros:**
- `x, y`: Coordenadas do canto superior esquerdo
- `largura, altura`: Dimensões em pixels
- `texto`: Texto centralizado no botão
- `cor_fundo`: Tupla RGB (R, G, B)
- `cor_texto`: Tupla RGB

**Cálculo da Cor Hover:**
```python
cor_hover = (max(0, R-30), max(0, G-30), max(0, B-30))
```
Escurece cada componente em 30, com mínimo de 0.

**Exemplo:**
```python
cor_fundo = (238, 228, 218)
cor_hover = (208, 198, 188)  # -30 em cada componente
```

---

#### `desenhar(self, tela, fonte)`

**Propósito:** Renderiza botão com efeito hover.

**Parâmetros:**
- `tela`: pygame.Surface onde desenhar
- `fonte`: pygame.font.Font para o texto

**Processo:**
1. Obtém posição do mouse
2. Verifica se mouse está sobre botão (`collidepoint`)
3. Escolhe cor (hover ou normal)
4. Desenha retângulo com `border_radius=10`
5. Renderiza texto centralizado

**Centralização do Texto:**
```python
texto_rect.center = self.rect.center
```
Garante texto sempre no centro, independente do tamanho.

---

#### `foi_clicado(self, evento)`

**Propósito:** Verifica se botão foi clicado.

**Retorno:** `True` se clicado, `False` caso contrário.

**Condições para Clique Válido:**
1. `evento.type == pygame.MOUSEBUTTONDOWN` (mouse pressionado)
2. `evento.button == 1` (botão esquerdo)
   - 1 = esquerdo, 2 = meio (scroll), 3 = direito
3. `self.rect.collidepoint(evento.pos)` (clique dentro da área)

**Uso Típico:**
```python
for evento in pygame.event.get():
    if btn_novo_jogo.foi_clicado(evento):
        iniciar_novo_jogo()
```

---

### Classe GerenciadorRanking (src/gerenciador_ranking.py)

#### `__init__(self, arquivo_ranking)`

**Propósito:** Inicializa gerenciador com caminho do arquivo.

**Parâmetros:**
- `arquivo_ranking`: Caminho (relativo ou absoluto) do arquivo

**Nota:** Arquivo não precisa existir, será criado na primeira gravação.

---

#### `carregar_pontuacao_maxima(self)`

**Propósito:** Retorna maior pontuação do histórico.

**Algoritmo:**
1. Verifica se arquivo existe
2. Lê todas as linhas
3. Para cada linha, extrai pontuação (parse por '|')
4. Retorna máximo

**Formatos Suportados:**
- `"Nome|Pontuação"` (padrão)
- `"Pontuação"` (legado)

**Tratamento de Erros:**
- Arquivo não existe: retorna 0
- Arquivo vazio: retorna 0
- Linha mal formatada: ignora e continua
- Erro de I/O: imprime erro, retorna 0

**Complexidade:**
- Tempo: O(n) onde n = número de linhas
- Espaço: O(n) para lista temporária de pontuações

---

#### `salvar_pontuacao(self, nome, pontuacao)`

**Propósito:** Adiciona entrada ao ranking.

**Parâmetros:**
- `nome`: Nome do jogador (pode ter espaços)
- `pontuacao`: Pontuação alcançada

**Formato de Saída:** `"Nome | Pontuação\n"`

**Modo de Abertura:** 'a' (append)
- Adiciona ao final (não sobrescreve)
- Cria arquivo se não existir
- Fecha automaticamente via `with`

**Nota:** Não ordena nem valida duplicatas. Ordenação é feita em `ler_ranking()`.

---

#### `ler_ranking(self)`

**Propósito:** Retorna lista formatada com top 15 pontuações.

**Retorno:** Lista de strings formatadas, ou `["Ranking vazio."]`

**Algoritmo:**
1. Lê arquivo
2. Parse de cada linha (separa por '|')
3. Cria lista de tuplas `(nome, pontuação)`
4. Ordena por pontuação (decrescente)
5. Limita aos 15 melhores
6. Formata cada entrada: `"1. Nome        Pontuação"`

**Formato de Saída:**
```
 1. Pieper               2352
 2. Christian            2184
 3. Jogador              1536
```

**Tratamento de Erros:**
- Arquivo não existe: retorna `["Ranking vazio."]`
- Erro de I/O: retorna `["Erro ao ler ranking."]`

---

### Classe EstadoBase (estados/estado_base.py)

#### `__init__(self, jogo)`

**Propósito:** Inicializa estado com referência ao jogo principal.

**Parâmetros:**
- `jogo`: Instância da classe Jogo

**Nota:** Todos estados concretos devem chamar `super().__init__(jogo)`.

---

#### `processar_eventos(self, evento)` (abstrato)

**Propósito:** Trata eventos específicos do estado.

**Parâmetros:**
- `evento`: pygame.event.Event

**Implementação Base:** `pass` (não faz nada)

**Responsabilidade das Subclasses:** Implementar comportamento específico.

**Exemplo (EstadoJogando):**
```python
def processar_eventos(self, evento):
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_LEFT:
            self.jogo.grade.mover_esquerda()
```

---

#### `desenhar(self, tela)` (abstrato)

**Propósito:** Renderiza o estado na tela.

**Parâmetros:**
- `tela`: pygame.Surface

**Implementação Base:** `pass`

**Padrão Overlay:** Alguns estados desenham sobre outros:
- EstadoVitoria desenha sobre EstadoJogando
- EstadoFimDeJogo desenha sobre EstadoJogando
- EstadoConfirmarSaida desenha sobre estado anterior

Isso cria efeito de sobreposição semitransparente.

---

| EstadoConfirmarSaida| Confirmação antes de sair          | → Estado anterior, ou Encerrar    |

---

## Algoritmos Principais

### 1. Algoritmo de Movimento e Fusão

**Entrada:** Linha do tabuleiro  
**Saída:** Linha após movimento + pontos ganhos

**Pseudocódigo:**
```
função mover_linha_esquerda(linha):
    # Fase 1: Compressão
    nova_linha ← [elemento para elemento em linha se elemento ≠ 0]
    pontos ← 0
    
    # Fase 2: Fusão
    i ← 0
    enquanto i < comprimento(nova_linha) - 1:
        se nova_linha[i] = nova_linha[i+1]:
            nova_linha[i] ← nova_linha[i] * 2
            pontos ← pontos + nova_linha[i]
            remover nova_linha[i+1]
        i ← i + 1
    
    # Fase 3: Preenchimento
    enquanto comprimento(nova_linha) < tamanho:
        adicionar 0 ao final de nova_linha
    
    retornar (nova_linha, pontos)
```

**Exemplo de Execução:**
```
Entrada: [2, 0, 2, 4]

Fase 1 (Compressão):
[2, 0, 2, 4] → [2, 2, 4]

Fase 2 (Fusão):
i=0: nova_linha[0]=2, nova_linha[1]=2 → iguais!
     nova_linha[0] ← 4, pontos ← 4
     remove nova_linha[1]
     nova_linha = [4, 4]
i=1: fim do loop

Fase 3 (Preenchimento):
[4, 4] → [4, 4, 0, 0]

Saída: ([4, 4, 0, 0], 4)
```

### 2. Verificação de Game Over

**Algoritmo:**
```
função pode_mover():
    # Verifica células vazias
    para cada célula em matriz:
        se célula = 0:
            retornar verdadeiro
    
    # Verifica fusões horizontais
    para cada linha em matriz:
        para cada célula em linha (exceto última):
            se célula = próxima_célula:
                retornar verdadeiro
    
    # Verifica fusões verticais
    para cada coluna em matriz:
        para cada célula em coluna (exceto última):
            se célula = célula_abaixo:
                retornar verdadeiro
    
    retornar falso  # Game Over!
```

**Complexidade:** O(n²)

### 3. Transposição de Matriz (para movimento vertical)

**Python idiomático usando zip:**
```python
# Transpor matriz (linhas ↔ colunas)
matriz_transposta = [list(col) for col in zip(*matriz)]
```

**Como funciona:**
```python
# Entrada
matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# zip(*matriz) desempacota e agrupa
# zip([1,2,3], [4,5,6], [7,8,9])
# → [(1,4,7), (2,5,8), (3,6,9)]

# Convertendo para listas
transposta = [
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9]
]
```

---

## Fluxo de Estados

### Diagrama de Transições

```
                    ┌─────────────────┐
                    │   EstadoMenu    │
                    │   (Inicial)     │
                    └────────┬─────────┘
                             │
                  ┌──────────┼──────────┐
                  │                     │
         [Novo Jogo]              [Ver Ranking]
                  │                     │
          ┌───────▼──────────┐  ┌──────▼──────┐
          │ EstadoJogando    │  │EstadoRanking│
          │                  │  │             │
          │ [Setas: mover]   │  │[Tecla: sair]│
          │ [U: desfazer]    │  └──────┬──────┘
          │ [ESC: sair]      │         │
          └─────┬──┬─────────┘         │
                │  │                   │
    ┌───────────┘  └───────────┐       │
    │                          │       │
[Vitória]                  [GameOver]  │
    │                          │       │
┌───▼──────────┐      ┌────────▼────┐  │
│EstadoVitoria │      │EstadoFimJogo│  │
│              │      │             │  │
│[C: continuar]│      │[Tecla:nome] │  │
│[M: menu]     │      └──────┬──────┘  │
└──────────────┘             │         │
                    ┌────────▼────────┐│
                    │EstadoInserirNome││
                    │                 ││
                    │[Enter: salvar]  ││
                    └────────┬─────────┘
                             │
                             └─────────┘

                    [ESC em qualquer estado]
                             │
                    ┌────────▼──────────┐
                    │EstadoConfirmarSaída│
                    │                   │
                    │[S: sair]          │
                    │[N: cancelar]      │
                    └───────────────────┘
```

### Tabela de Transições

| Estado Atual       | Evento              | Próximo Estado      |
|--------------------|---------------------|---------------------|
| Menu              | Clicar "Novo Jogo"  | Jogando            |
| Menu              | Clicar "Ranking"    | Ranking            |
| Menu              | Pressionar ESC      | ConfirmarSaída     |
| Jogando           | Atingir 2048        | Vitória            |
| Jogando           | Sem movimentos      | FimDeJogo          |
| Jogando           | Pressionar ESC      | ConfirmarSaída     |
| Vitória           | Pressionar C        | Jogando (continua) |
| Vitória           | Pressionar M        | Menu               |
| FimDeJogo         | Qualquer tecla      | InserirNome        |
| InserirNome       | Pressionar Enter    | Ranking            |
| Ranking           | Qualquer tecla      | Menu               |
| ConfirmarSaída    | Pressionar S        | Encerra programa   |
| ConfirmarSaída    | Pressionar N/ESC    | Estado anterior    |

---

## Estruturas de Dados

### 1. Matriz do Jogo

**Tipo:** `list[list[int]]`

**Estrutura:**
```python
matriz = [
    [0, 2, 0, 4],    # Linha 0
    [2, 4, 8, 16],   # Linha 1
    [0, 0, 0, 0],    # Linha 2
    [2, 0, 2, 0]     # Linha 3
]
# Acesso: matriz[linha][coluna]
# matriz[1][2] = 8
```

**Convenções:**
- 0 = célula vazia
- 2, 4, 8, ..., 2048 = valores das peças

### 2. Dados de Ranking

**Formato em Memória:**
```python
# Lista de tuplas (nome, pontuação)
dados = [
    ("Pieper", 2352),
    ("Christian", 2184),
    ("Jogador", 1536)
]
```

**Formato no Arquivo:**
```
Pieper|2352
Christian|2184
Jogador|1536
```

### 3. Dicionário de Cores

**Estrutura:**
```python
CORES = {
    # Valores das peças
    0: (205, 193, 180),     # Célula vazia
    2: (238, 228, 218),     # Peça 2
    4: (237, 224, 200),     # Peça 4
    ...
    2048: (237, 194, 46),   # Peça 2048
    
    # Cores da UI
    'fundo': (187, 173, 160),
    'texto_escuro': (119, 110, 101),
    'texto_claro': (249, 246, 242)
}
```

---

## Como Executar

### Requisitos

- Python 3.7+
- Pygame 2.0+

### Instalação

```bash
# Instalar Pygame
pip install pygame

# Ou usando requirements.txt
pip install -r requirements.txt
```

### Executar o Jogo

```bash
python3 2048_jogo.py
```

### Controles

**No Menu:**
- Clique nos botões com o mouse

**Durante o Jogo:**
- `←, →, ↑, ↓`: Mover peças
- `U`: Desfazer último movimento
- `ESC`: Confirmar saída

**Na Vitória:**
- `C`: Continuar jogando
- `M`: Voltar ao menu

**Inserir Nome:**
- Digite o nome
- `Enter`: Confirmar
- `Backspace`: Apagar

---

## Como Estender

### Adicionar Novo Estado

1. **Criar nova classe em `estados/`:**
```python
class EstadoNovoEstado(EstadoBase):
    def __init__(self, jogo):
        super().__init__(jogo)
        # Inicialização específica
    
    def processar_eventos(self, evento):
        # Lógica de eventos
        pass
    
    def desenhar(self, tela):
        # Lógica de desenho
        pass
```

2. **Importar no estado que transiciona:**
```python
from estados.estado_novo_estado import EstadoNovoEstado
```

3. **Adicionar transição:**
```python
if condicao:
    self.jogo.transicionar_para(EstadoNovoEstado(self.jogo))
```

### Modificar Tamanho da Grade

Em `src/configuracoes.py`:
```python
TAMANHO_GRADE = 5  # Muda para 5x5
```

**Nota:** Pode ser necessário ajustar cores e fontes para peças maiores.

### Adicionar Novos Botões

```python
# Em __init__ do estado
self.meu_botao = Botao(x, y, largura, altura, 
                       "Texto", cor_fundo, cor_texto)

# Em processar_eventos
if self.meu_botao.foi_clicado(evento):
    # Ação do botão

# Em desenhar
self.meu_botao.desenhar(tela, fonte)
```

### Adicionar Animações

Adicionar atributos de tempo em `__init__`:
```python
self.tempo_inicio = pygame.time.get_ticks()
```

Em `desenhar`, calcular animação:
```python
tempo_atual = pygame.time.get_ticks()
tempo_decorrido = tempo_atual - self.tempo_inicio
alpha = min(255, tempo_decorrido // 2)  # Fade in
```

---

## Análise de Complexidade

### Operações Principais

| Operação                  | Complexidade | Explicação                           |
|---------------------------|-------------|--------------------------------------|
| Movimento (qualquer dir.) | O(n²)       | Processa todas as células           |
| Verificar game over       | O(n²)       | Varre toda a matriz                 |
| Gerar nova peça          | O(n²)       | Busca células vazias                |
| Maior peça               | O(n²)       | Procura max em toda matriz          |
| Salvar/Carregar estado   | O(n²)       | Deepcopy da matriz                  |

### Uso de Memória

- **Matriz principal**: O(n²) ≈ 16 células (4x4)
- **Matriz desfazer**: O(n²) ≈ 16 células (cópia)
- **Total por Grade**: ~256 bytes

**Nota:** n = TAMANHO_GRADE (padrão: 4)

---

## Boas Práticas Implementadas

### 1. Docstrings Completas
Todas as classes e métodos possuem documentação detalhada

### 2. Type Hints (Implícitas)
Documentação clara dos tipos esperados

### 3. Separation of Concerns
Cada módulo/classe tem responsabilidade única

### 4. DRY Principle
Código reutilizável em módulos utils

### 5. Error Handling
Tratamento robusto de exceções em I/O

### 6. Naming Conventions
Nomes descritivos em português (conforme solicitado)

### 7. Constants Centralization
Todas as constantes em `configuracoes.py`

---

## Possíveis Melhorias Futuras

1. **Animações de Movimento**
   - Transições suaves entre posições
   - Efeitos de fusão

2. **Sistema de Conquistas**
   - Badges por marcos alcançados
   - Estatísticas detalhadas

3. **Temas Personalizáveis**
   - Diferentes paletas de cores
   - Modos claro/escuro

4. **Multiplayer Local**
   - Dois jogadores alternando turnos
   - Competição por maior pontuação

5. **Salvamento Automático**
   - Continuar jogo após fechar
   - Múltiplos slots de save

6. **Sons e Música**
   - Efeitos sonoros para movimentos
   - Música de fundo

7. **Modos de Jogo**
   - Modo zen (sem game over)
   - Modo tempo limitado
   - Desafios diários

8. **Rede Neural para IA**
   - Bot que joga automaticamente
   - Modo de aprendizado

---

## Referências

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Python Official Documentation](https://docs.python.org/3/)
- [Game Programming Patterns](https://gameprogrammingpatterns.com/)
- [2048 Original Game](https://play2048.co/)

---

## Contato

**Christian Pieper**  
UniSenac - Algoritmos e Estruturas de Dados I  
Novembro de 2025

---

*Esta documentação foi gerada com assistência de IA para garantir completude e clareza.*
