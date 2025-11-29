# AFD/AFN — Operadores e Símbolos

## Padrões tratados
- Pontuação: `;` `,` `{` `}` `(` `)` são tokens de único caractere.
- Símbolos especiais usados na linguagem: 'x' para dimensões (ex: 800x600).

## AFN
- Cada símbolo é reconhecido diretamente como literal (transição do estado inicial para estado aceitação).
- Não há complexidade adicional aqui — o lexer prioriza strings e números, depois identifica símbolos únicos.

## Observação
- Na implementação final, símbolos são tratados explicitamente no driver de tokenização para evitar ambiguidade com identifiers ou strings.
