
# IMAGELANG — Manual de Utilização

Este manual descreve como escrever programas na linguagem **Imagelang**, como compilá-los para Python e como executá-los usando o compilador que você enviou.

## Visão Geral

Imagelang é uma DSL (linguagem específica de domínio) para **processamento de imagens** construída sobre OpenCV e NumPy. Ela possui comandos de alto nível (em português) que correspondem a funções no runtime (`il_runtime.py`). O pipeline do compilador é:

```
Fonte (.il) -> Lexer (lexer_afn.py) -> Parser (parser.py) -> Análise Semântica (semantic_analyzer.py) -> Codegen (to_python.py) -> Python (.py)
```

## Estrutura de um Programa

- Cada comando termina com `;` (ponto e vírgula).
- Strings são escritas entre aspas `"..."`.
- Identificadores representam variáveis de imagem (ex.: `img1`, `resultado`).
- Muitos comandos seguem o padrão `comando <src> ... como <dst>;` onde `<src>` é a variável de entrada e `<dst>` é a variável de saída.

### Exemplo completo

```imagelang
// Carrega, redimensiona, aplica filtro e salva
abrir_imagem "entrada.jpg" como img;
redimensionar img para 640 x 480 como img_res;
aplicar_filtro img_res filtro "gaussiano" raio 5 como img_blur;
adicionar_texto img_blur texto "Demo" em 20, 40 tamanho 1.0 cor 255,255,255 espessura 2;
salvar_imagem img_blur em "saida.jpg";
```

## Compilação e Execução

### Compilar

Use o CLI (`main.py`) para compilar:

```bash
python main.py compile caminho/programa.imgl -o programa.py
```

O arquivo Python gerado será salvo em `out/programa.py`.

### Executar diretamente

```bash
python main.py executar caminho/programa.imgl
```

O comando acima compila para um arquivo temporário e já executa o script.

## Convenções e Erros Comuns

- **Variáveis não definidas**: a análise semântica exige que toda variável usada já tenha sido produzida por algum comando anterior (ex.: `Abrir`) — caso contrário, um `SemanticError` será lançado.
- **Tipos de parâmetros**: números inteiros para coordenadas e tamanhos; `float` para valores como `gamma`, `alpha` e escalas.
- **Coordenadas e tamanhos**: comandos que recebem coordenadas (`x, y`) e dimensões (`w, h`) usam pixels inteiros.

## Saída e Persistência

- Use `salvar_imagem <id> em "arquivo.ext";` para gravar a imagem.
- Algumas operações retornam coleções (ex.: `detectar_faces` retorna lista de caixas), que podem ser usadas em comandos subsequentes como `desenhar_bbox`.

## Dicas de Uso

- Utilize `resize_max` para adequar imagens muito grandes antes de detectar bordas/contornos.
- Converta para cinza com `converter_para_gray` antes de certos filtros de detecção.
- Para sobreposição com transparência, prefira imagens com canal alfa ou utilize `alpha` em `overlay_image`.

