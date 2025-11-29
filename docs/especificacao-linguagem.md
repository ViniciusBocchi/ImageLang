# Especificação da Linguagem ImageLang (.il)

Versão resumida — contém tokens, sintaxe e semântica dos comandos suportados.

## Tokens
- Literais:
  - STRING: texto entre aspas duplas, exemplo: "foto.jpg"
  - NUMBER: sequência de dígitos, pode ter decimal: 123 ou 12.5
  - IDENT: identificador (letras, dígitos, underscore), exemplo: img1
- Palavras-chave (case-sensitive na implementação atual): `abrir_imagem`, `salvar_imagem`, `como`, `rotacionar`, `por`, `redimensionar`, `para`, `cortar`, `aplicar_filtro`, `filtro`, `raio`, `adicionar_texto`, `texto`, `em`, `tamanho`, `cor`, `espessura`, `sobrepor`, `com`, `alpha`
- Símbolos: `;` `,` `{` `}` `(` `)` e `x` usado em dimensões.

## Sintaxe (exemplos)

- Abrir imagem:
  ```
  abrir_imagem "caminho.jpg" como img;
  ```

- Salvar imagem:
  ```
  salvar_imagem img em "saida.jpg";
  ```

- Rotacionar:
  ```
  rotacionar img por 45 como img_rot;
  ```

- Redimensionar:
  ```
  redimensionar img para 800x600 como img_res;
  ```

- Cortar:
  ```
  cortar img para 10,20,100,200 como img_cut;
  ```

- Aplicar filtro:
  ```
  aplicar_filtro img filtro "gaussiano" raio 5 como img_f;
  ```

- Adicionar texto:
  ```
  adicionar_texto img texto "Olá" em 10,20 tamanho 24 cor 255,255,255 espessura 2;
  ```

- Sobrepor:
  ```
  sobrepor base com overlay em 10,20 alpha 0.6 como resultado;
  ```

## Semântica
- Identificadores devem ser definidos (por `abrir_imagem` ou por operações que retornem imagens) antes do uso.
- Tipos de argumentos: `STRING` para caminhos; `NUMBER` para números; `IDENT` para variáveis imagem.
- Erros semânticos levam a mensagens e falha na compilação.

## Operações suportadas (mapeadas para il_runtime)
- abrir_imagem, salvar_imagem, rotacionar, redimensionar, cortar, aplicar_filtro, adicionar_texto, sobrepor, ajustar_brilho_contraste, detectar_bordas, equalizar_histograma, converter_canal

Para a especificação completa (formas de extensão e gramática formal LL(1)) consulte `docs/arquitetura.md` e `docs/guia-desenvolvimento.md`.
