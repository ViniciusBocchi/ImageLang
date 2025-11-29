# AFD/AFN — Número

## Descrição do padrão
Número inteiro ou decimal: sequência de dígitos, opcionalmente com '.' seguido por dígitos.

Regex: `[0-9]+(\.[0-9]+)?`

## AFN (conceitual)
- q0 -> (dígito) -> q1 (aceitação)
- q1 -> (dígito) -> q1
- q1 -> '.' -> q2
- q2 -> (dígito) -> q3 (aceitação)
- q3 -> (dígito) -> q3

## Conversão para AFD
- Subconjuntos relevantes: {q0},{q1},{q2},{q3} e combinações resultantes.
- AFD final aceita inteiros e decimais.

## Implementação
- Veja `nfa_number()` em `src/ilc/lexer/lexer_afn.py`.
