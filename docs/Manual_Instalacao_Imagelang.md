
# IMAGELANG — Manual de Instalação e Roteiro (para leigos)

Este guia foi escrito para quem **nunca** configurou Python/OpenCV. Siga passo a passo.

## 1) Pré-requisitos

- **Python 3.10+** instalado.
- **pip** funcionando.
- Acesso à internet para baixar dependências.

## 2) Baixar o projeto

1. Crie uma pasta de trabalho (ex.: `C:\\Imagelang` ou `~/Imagelang`).
2. Copie/clonar os arquivos do compilador para dentro dessa pasta (conforme estrutura mostrada no VS Code).

## 3) Criar ambiente virtual (recomendado)

Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
Linux/macOS (bash):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4) Instalar dependências

Dentro do ambiente virtual, rode:

```bash
pip install opencv-python numpy
```

> Se quiser efeitos `oil_painting` com `cv2.xphoto`, pode ser necessário `opencv-contrib-python`:
```bash
pip install opencv-contrib-python
```

## 5) Testar a instalação

No terminal, dentro da pasta do projeto, execute:

```bash
python -c "import cv2, numpy as np; print('OK OpenCV', cv2.__version__)"
```

Se aparecer algo como `OK OpenCV 4.x.x`, está tudo certo.

## 6) Compilar um exemplo

1. Crie um arquivo `examples/test_basico.imgl` com o conteúdo:
```imagelang
abrir_imagem "examples/imagens/lena.png" como src;
redimensionar src para 512 x 512 como r1;
clahe r1 clip 2.0 tile 8,8 como r2;
salvar_imagem r2 em "out/saida.png";
```
2. Execute a compilação:
```bash
python main.py compile examples/test_basico.imgl -o saida.py
```
3. Rode o Python gerado:
```bash
python out/saida.py
```
4. Verifique se `out/saida.png` foi criado.

## 7) Executar direto (atalho)

```bash
python main.py executar examples/test_basico.imgl
```

## 8) Problemas comuns

- **Falha ao abrir imagem**: verifique o caminho/arquivo existe.
- **Permissão ao salvar**: garanta que a pasta `out/` existe ou que você tem permissão.
- **ImportError**: confirme que está no ambiente virtual ativado e que `opencv-python` foi instalado.

## 9) Estrutura recomendada de pastas

```
IMAGELANG_COMPILADOR_FULL/
  main.py
  frontend.py
  ilc/
    lexer/lexer_afn.py
    parser/parser.py
    semantic/semantic_analyzer.py
    codegen/to_python.py
    runtime/
      il_runtime.py
      buffer_otimizado.py
  examples/
    imagens/
    test_basico.py (ou .imgl)
  out/
```

Pronto! Você já consegue compilar e executar programas Imagelang.
