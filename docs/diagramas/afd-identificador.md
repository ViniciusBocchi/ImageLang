# AFD/AFN — Identificador

Este documento descreve o autômato finito não-determinístico (AFN) e o AFD resultante para reconhecer identificadores.

## Descrição do padrão
Um identificador é: letra ou underscore seguido por letras, dígitos ou underscores.

Regex equivalente: `[A-Za-z_][A-Za-z0-9_]*` (apenas para referência).

## AFN (conceitual)
- Estado q0: início.
- Transições por qualquer letra ou '_' de q0 para q1.
- Estado q1: estado aceitação; de q1 há transições por letras/dígitos/'_' para q1 (loop).

## Conversão para AFD
- Após subset-construction, o AFD terá:
  - Estado {q0} como não-aceitante.
  - Estado {q1} como aceitante.
  - Possivelmente um estado de erro (dead state) para símbolos não esperados.

## Observações
- Implementação no código: `src/ilc/lexer/lexer_afn.py` (função `nfa_identifier`).
