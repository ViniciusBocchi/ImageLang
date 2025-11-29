
# IMAGELANG — Listagem de Comandos

Abaixo estão todos os comandos suportados pelo **parser** e **runtime**, com a sintaxe básica.

> **Nota**: sempre finalize com `;`.

## IO
- `abrir_imagem "caminho" como <id>;`
- `salvar_imagem <id> em "caminho";`

## Transformações Geométricas
- `rotacionar <src> por <graus> como <dst>;`
- `redimensionar <src> para <largura> x <altura> como <dst>;`
- `redimensionar <src> por <fx> <fy> como <dst>;`
- `cortar <src> para <x>,<y>,<w>,<h> como <dst>;`
- `transladar <src> por <dx>,<dy> como <dst>;`
- `espelhar <src> horizontal|vertical|both como <dst>;`
- `warp_perspectiva <src> para x1,y1, x2,y2, x3,y3, x4,y4 como <dst>;`
- `remap <src> <mapx> <mapy> como <dst>;`

## Filtros e Denoise
- `aplicar_filtro <src> filtro "nome" [raio <r>] como <dst>;` (gaussiano, mediana, bilateral, laplacian, sobel, sharpen, emboss)
- `desfocar <src> <k> como <dst>;`
- `mediana <src> <k> como <dst>;`
- `bilateral <src> <d> como <dst>;`
- `remover_ruido <src> [<h>] como <dst>;`

## Ajustes
- `ajustar_brilho_contraste <src> brilho <b> contraste <c> como <dst>;`
- `ajustar_gamma <src> gamma <g> como <dst>;`
- `clahe <src> [clip <c>] [tile <w>,<h>] como <dst>;`

## Canais e Cores
- `converter_canal <src> "CODIGO" como <dst>;` (ex.: `BGR2RGB`, `BGR2GRAY` etc.)
- `bgr_to_rgb <src> como <dst>;`
- `rgb_to_bgr <src> como <dst>;`
- `converter_para_gray <src> como <dst>;`

## Detecção / Bordas / Contornos
- `detectar_bordas <src> [metodo "canny|laplacian|sobel"] [threshold1 <t1>] [threshold2 <t2>] [aperture <k>] como <dst>;`
- `detectar_contornos <src> [min_area <n>] como <dst>;`
- `desenhar_contornos <src> <contours> [cor r,g,b] [espessura n] como <dst>;`
- `detectar_circulos <src> como <dst>;`
- `detectar_retangulos <src> como <dst>;`

## Morfologia
- `morfologia <src> operacao "erode|dilate|open|close|gradient|tophat|blackhat" [ksize <k>] [iterations <n>] [shape "rect|ellipse|cross"] como <dst>;`
- Atalhos:
  - `erodir <src> [ksize <k>] como <dst>;`
  - `dilatar <src> [ksize <k>] como <dst>;`
  - `abrir_morf <src> [ksize <k>] como <dst>;`
  - `fechar_morf <src> [ksize <k>] como <dst>;`

## Equalização / Histograma
- `equalizar_histograma <src> como <dst>;`
- `equalizar_color <src> como <dst>;`
- `histograma <src> [canal <c>] como <dst>;`
- `equalizar_clahe <src> [clip <c>] [tile <w>,<h>] como <dst>;`

## Segmentação
- `thresholding <src> [metodo "otsu|binary|adaptive"] [thresh <n>] [tipo "binary|binary_inv"] como <dst>;`
- `kmeans_segmentacao <src> [k <n>] como <dst>;`
- `grabcut_remover_fundo <src> [rect x,y,w,h] [iter <n>] como <dst>;`

## Efeitos Artísticos
- `cartoonize <src> como <dst>;`
- `pencil_sketch <src> como <dst>;` (gera `<dst>_gray` e `<dst>_color`)
- `oil_painting <src> como <dst>;`

## Faces
- `detectar_faces <src> como <dst>;`
- `desenhar_bbox <src> <bboxes> [cor r,g,b] [espessura n] como <dst>;`

## Blending / Overlay
- `alpha_blend <fg> com <bg> [alpha <a>] como <dst>;`
- `overlay_image <base> com <overlay> em <x>,<y> [alpha <a>] como <dst>;`
- `overlay_text <src> "texto" em <x>,<y> [font <s>] [cor r,g,b] [espessura n] [bgcolor r,g,b] como <dst>;`

## Utilitários
- `resize_max <src> <max_size> como <dst>;`
- `ensure_color <src> como <dst>;`
- `to_bytes <src> [ext ".png"] como <dst>;`
