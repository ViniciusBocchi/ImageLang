# Guia da Linguagem ImageLang

A **ImageLang** é uma linguagem simples e declarativa para manipulação
de imagens.\
Ela permite abrir, redimensionar, aplicar filtros, sobrepor imagens e
salvar resultados.

------------------------------------------------------------------------

## 📌 Estrutura Geral

Cada instrução termina com ponto e vírgula `;`.

    comando argumentos... ;

------------------------------------------------------------------------

## 📂 Comandos Disponíveis

### 1. **abrir_imagem**

Abre uma imagem do disco e armazena em uma variável.

    abrir_imagem "caminho/arquivo.jpg" como nome_variavel;

**Exemplo:**

    abrir_imagem "examples/imagens/foto1.jpg" como img;

------------------------------------------------------------------------

### 2. **redimensionar**

Redimensiona uma imagem para largura × altura.

    redimensionar img para LARGURAxALTURA como nova_img;

**Exemplo:**

    redimensionar img para 400x300 como img_r;

------------------------------------------------------------------------

### 3. **aplicar_filtro**

Aplica um filtro específico na imagem.

    aplicar_filtro img filtro "tipo" raio N como nova_img;

Filtros disponíveis podem incluir: - gaussiano - suavizacao - nitidez -
contorno

**Exemplo:**

    aplicar_filtro img_r filtro "gaussiano" raio 5 como img_blur;

------------------------------------------------------------------------

### 4. **sobrepor**

Sobrepõe uma imagem sobre outra nas coordenadas X×Y.

    sobrepor imagem_base em XxY como imagem_final;

**Exemplo:**

    sobrepor img_blur em 10,20 como img_final;

------------------------------------------------------------------------

### 5. **salvar_imagem**

Salva uma variável de imagem em um arquivo.

    salvar_imagem img_final em "out/resultado.jpg";

------------------------------------------------------------------------

## 🧪 Exemplo Completo

    abrir_imagem "examples/imagens/foto1.jpg" como img;
    redimensionar img para 400x300 como img_r;
    aplicar_filtro img_r filtro "gaussiano" raio 5 como img_blur;
    sobrepor img_blur em 10x20 como img_final;
    salvar_imagem img_final em "out/demo_result.jpg";

------------------------------------------------------------------------

## ▶️ Como Compilar e Executar

No terminal, dentro da pasta **ilc**:

### **Compilar um arquivo .il:**

    python ilc/main.py compile examples/arquivo .il -o saida.py

### **Executar arquivo:**

    python python out/saida.py

------------------------------------------------------------------------

## ✔️ Observações

-   Todos os comandos exigem `;` no final.
-   Coordenadas e redimensionamento usam `L,A`.
-   Variáveis não podem conter espaços.
-   Os caminhos devem estar entre aspas.

------------------------------------------------------------------------

Pronto! Agora você já pode escrever seus próprios programas ImageLang.
