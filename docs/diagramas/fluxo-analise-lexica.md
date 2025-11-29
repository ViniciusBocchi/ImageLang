# Fluxo — Análise Léxica (alto nível)

1. **Leitura do arquivo**: caracteres são lidos sequencialmente.
2. **Ignorar espaços e comentários**: espaços e comentários `//` são descartados.
3. **Detectar strings**: quando encontra '"' inicia leitura de STRING (com suporte a escape `\`).
4. **Detectar números**: sequências que começam com dígito são lidas como NUMBER (suportam ponto decimal).
5. **Detectar identifiers/keywords**: palavras que começam com letra/underscore são lidas e comparadas com a tabela de KEYWORDS.
6. **Detectar símbolos/operadores**: se houver caracteres especiais (';', ',', 'x', etc) são retornados como tokens.
7. **Token EOF**: ao final um token EOF é gerado.

## Nota sobre AFN→AFD
- Embora o projeto contenha funções para construir NFAs para vários padrões, o driver de tokenização usa uma combinação prática: ele usa NFAs para tipos complexos (identificadores, números, strings) e trata símbolos e palavras-chave no fluxo principal.
- Para extensões que exijam cobertura completa AFN→AFD (ex.: suporte a expressões regulares arbitrárias), recomenda-se a implementação de um gerador de AFD global que una todos os AFNs e execute a construção do DFA minimizado. Isso está documentado em `docs/guia-desenvolvimento.md`.

