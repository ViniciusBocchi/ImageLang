# 📘 Projeto Integrador – Linguagem para Manipulação de Imagens

## 📋 Objetivos da Semana
- Aplicar conceitos de **alfabetos, palavras e linguagens** na definição formal dos elementos básicos da linguagem.  
- Definir o **alfabeto básico** da linguagem (quais caracteres são válidos).  
- Especificar os diferentes tipos de **tokens** (identificadores, números, operadores, palavras-chave).  
- Explorar operações com linguagens formais para compor tokens complexos.  
- Aplicar o conceito de **fechamento de Kleene** para definir elementos de comprimento variável, como strings, comentários e listas de parâmetros.  

---

## 🎯 Atividades do Projeto Integrador
Esta semana marca o início da **especificação formal da linguagem**.  
As principais atividades serão:  

1. **Definição do Alfabeto Básico**  
   - Letras (a-z, A-Z, acentuadas em português como á, ç, ã).  
   - Dígitos (0-9).  
   - Operadores e símbolos especiais: `=`, `+`, `-`, `*`, `/`, `"`, `()`.  
   - Espaço em branco, tabulação e quebras de linha.  

2. **Tipos de Tokens**  
   - **Palavras-chave**: `abrir`, `salvar`, `aumentar`, `diminuir`, `brilho`, `contraste`, `recortar`, `girar`, `imagem`.  
   - **Identificadores**: nomes definidos pelo usuário para variáveis (ex.: `foto1`, `minha_imagem`).  
   - **Literais Numéricos**: inteiros (`10`), decimais (`10.5`), notação científica (`1.2e3`).  
   - **Strings**: delimitadas por aspas duplas (`"foto.png"`).  
   - **Comentários**: iniciados por `#` e válidos até o fim da linha.  

3. **Estrutura Léxica Geral**  
   - Um programa é composto por uma sequência de instruções, cada uma em uma linha.  
   - Exemplo:  
     ```
     abrir_imagem "foto.png"
     aumentar_brilho "foto.png" 20
     salvar_imagem "nova_foto.png"
     ```

4. **Uso das Operações de Linguagens**  
   - **Fechamento de Kleene**: definir strings de qualquer tamanho (`"a"`, `"abc"`, `"arquivo.png"`).  
   - **Concatenação**: instruções são compostas de tokens concatenados (ex.: `abrir` + `imagem` + `"foto.png"`).  
   - **União**: diferentes palavras-chave pertencem ao mesmo conjunto de comandos válidos.  

---

## 💡 Reflexões Importantes
- **Case-sensitive ou case-insensitive?**  
  → A linguagem será **case-insensitive**, ou seja, `ABRIR` e `abrir` são equivalentes, para facilitar a escrita.  

- **Caracteres permitidos em strings**  
  → Strings aceitam letras, números, acentos, símbolos especiais e espaços entre aspas.  

- **Tratamento de espaços em branco e quebras de linha**  
  → Espaços extras entre tokens serão ignorados, mas cada comando precisa terminar com uma quebra de linha.  

- **Ambiguidades potenciais**  
  - Identificadores **não podem começar com números** para evitar confusão com literais numéricos.  
  - Exemplo válido: `foto1`  
  - Exemplo inválido: `1foto`  

---

## 📊 Entrega da Semana
- [x] Especificação completa do **alfabeto da linguagem**  
- [x] Definição formal de todos os **tipos de tokens**  
- [x] Exemplos concretos de programas válidos  
- [x] Atualização do diário com decisões de design e justificativas  

---

## ✅ Exemplos de Programas Válidos

### Exemplo 1 – Abrir e salvar imagem
abrir_imagem "foto.png"
salvar_imagem "backup.png"

shell
Copiar
Editar

### Exemplo 2 – Ajuste de brilho e contraste
abrir_imagem "foto.png"
aumentar_brilho "foto.png" 30
diminuir_contraste "foto.png" 15
salvar_imagem "editada.png"

shell
Copiar
Editar

### Exemplo 3 – Recorte e rotação
abrir_imagem "paisagem.jpg"
recortar_imagem "paisagem.jpg" 100 200 400 500
girar_imagem "paisagem.jpg" 90
salvar_imagem "paisagem_editada.jpg"

yaml
Copiar
Editar

---

✍️ **Decisões de Design**
- Linguagem será em **português** para maior acessibilidade.  
- Foco em **simplicidade**: comandos curtos, intuitivos e próximos da linguagem natural.  
- Sintaxe inspirada em instruções diretas, como se o usuário estivesse “falando com o computador”.  