# Arquitetura do ImageLang Compiler

Este documento descreve a arquitetura do compilador **ImageLang (.il)**, versão completa.

## Visão geral em camadas

1. **Frontend**
   - **Lexer (AFN→AFD)**: transforma código-fonte em tokens. Implementado em `src/ilc/lexer/lexer_afn.py`.
   - **Parser (LL(1)-like)**: constrói a AST a partir dos tokens. Implementado em `src/ilc/parser/parser.py`.
   - **Analisador Semântica**: valida uso de identificadores e regras simples; `src/ilc/semantic/semantic_analyzer.py`.

2. **Codegen**
   - Tradução da AST para um script **Python** que usa o runtime (`src/ilc/codegen/to_python.py`).

3. **Runtime**
   - Biblioteca Python que implementa as operações de imagem (OpenCV) referenciadas pelos programas `.il` (`src/runtime/il_runtime.py`).

4. **CLI e Orquestração**
   - `src/main.py` e `src/ilc/frontend.py` controlam o fluxo: compilar e executar.

## Estruturas de dados principais

- **Token**: objeto com campos `type`, `value`, `line`, `col`.
- **NFA / AFN**: estados com transições por símbolo e transições epsilon.
- **DFA / AFD**: subconjuntos de estados NFA, construídos via subset-construction (implementado de forma pedagógica).
- **AST**: nós simples que descrevem comandos (Abrir, Salvar, Rotacionar, Redimensionar, Cortar, AplicarFiltro, AdicionarTexto, Sobrepor).

## Fluxo de execução (resumido)

1. Ler arquivo `.il`.
2. Tokenizar com o lexer AFN→AFD.
3. Parsear tokens para AST.
4. Análise semântica.
5. Gerar código Python (.py).
6. (Opcional) Executar o script gerado.

## Extensibilidade

- Adicionar novo comando:
  1. Atualizar gramática/parser (`src/ilc/parser/parser.py`).
  2. Adicionar semantic check (se necessário).
  3. Mapear para codegen (`src/ilc/codegen/to_python.py`).
  4. Implementar função correspondente no runtime (`src/runtime/il_runtime.py`).
