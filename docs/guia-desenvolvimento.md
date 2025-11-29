# Guia de Desenvolvimento — ImageLang

Este guia orienta como desenvolver, testar e estender o compilador.

## Requisitos
- Python 3.10+
- pip install -r requirements.txt

## Estrutura relevante
- `src/ilc/lexer/` — Lexer AFN→AFD
- `src/ilc/parser/` — Parser LL(1)-like
- `src/ilc/semantic/` — Regras semânticas
- `src/ilc/codegen/` — Gerador Python
- `src/runtime/` — Funções OpenCV

## Adicionando um novo token (palavra-chave)
1. Se o token for um literal, adicione-o à lista `KEYWORDS` em `lexer_afn.py`.
2. Ajuste o parser para tratar o novo token.
3. Atualize o codegen para mapear a nova AST node para chamadas em `il_runtime.py`.
4. Escreva testes unitários em `tests/`.

## Workflow de testes
- Executar testes unitários:
  ```bash
  pytest -q
  ```
- Rodar um exemplo:
  ```bash
  python src/main.py compile examples/02-demo-il.il -o out/demo.py
  python out/demo.py
  ```

## Boas práticas
- Cada mudança que altera a gramática deve ter testes sintáticos (parser) e testes de integração.
- Mantenha o runtime desacoplado: o codegen gera chamadas para o runtime; a lógica de processamento de imagem fica no `il_runtime`.
- Documente mudanças na pasta `docs/` e, quando alterar o lexer, atualize os diagramas AFN/AFD.
