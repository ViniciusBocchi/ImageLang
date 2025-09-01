# 🎯Conjuntos
## Conjunto de Terminais

```
T = {
    abrir, salvar, aplicar, mostrar, redimensionar, recortar, girar, espelhar,
    brilho, contraste, blur, nitidez, escala_cinza, inverter_cores, sepia,
    se, senao, enquanto, para, em, def, return, classe, fim,
    verdadeiro, falso, nao, e, ou,
    +, -, *, /, %, **, //,
    ==, !=, >, <, >=, <=,
    =,
    (, ), [, ], {, }, ,, :, ., ;,
    literal_inteiro, literal_real, literal_texto, literal_booleano,
    identificador
}
```

## Conjunto de Variáveis

```
V = {
    Programa, ListaComandos, Comando,
    Atribuicao, Expressao, Termo, Fator,
    ComandoImagem, Filtro, Condicional, Loop,
    ExpressaoLogica, OperadorRelacional,
    Funcao, ListaParametros, ListaArgumentos, Bloco
}
```

# 🏷 Classificação na Hierarquia de Chomsky
## 📖 Análise Formal da Classificação

- Analisei rigorosamente minha gramática e classifiquei-a como Tipo 2 (Livre de Contexto) na hierarquia de Chomsky:

#### Justificativa:

- ✅ Todas as produções têm a forma A → α (lado esquerdo sempre com um não-terminal).

- ✅ Não há dependências contextuais nas regras da gramática.

- ✅ A gramática descreve linguagens não regulares (devido a estruturas aninhadas como se...senao...fim e blocos indentados).

- ✅ É reconhecível por autômato de pilha, modelo formal equivalente a linguagens livres de contexto.

#### 🔍 Verificação

- ✅ Não é Tipo 3 (Regular):
Estruturas como condicionais e loops aninhados não podem ser expressas apenas com expressões regulares.

- ✅ É Tipo 2 (Livre de Contexto):
Todas as regras seguem o formato A → α, típico de CFG (Context-Free Grammar).

- ❌ Não precisa ser Tipo 1 (Sensível ao Contexto):
Não há regras da forma αAβ → αγβ (onde o contexto influencia a produção).
As checagens de tipo, escopo e uso de variáveis são semânticas, não sintáticas.

- ❌ Não precisa ser Tipo 0 (Irrestrita):
A gramática é bem estruturada e não necessita da generalidade máxima das linguagens irrestritas.


#### 📌 Exemplo de Derivação – Programa Simples com Estrutura Condicional

##### Programa:
```
abrir "foto.png"
se verdadeiro entao
    aplicar brilho
fim
```

#### Derivação Completa:
##### Programa
```
⇒ BlocoComandos
⇒ abrir literal_texto BlocoComandos
⇒ abrir "foto.png" BlocoComandos
⇒ abrir "foto.png" ComandoCondicional BlocoComandos
⇒ abrir "foto.png" se Expressao entao BlocoComandos fim BlocoComandos
⇒ abrir "foto.png" se ExpressaoLogica entao BlocoComandos fim BlocoComandos
⇒ abrir "foto.png" se literal_booleano entao BlocoComandos fim BlocoComandos
⇒ abrir "foto.png" se verdadeiro entao ComandoAplicacao BlocoComandos fim BlocoComandos
⇒ abrir "foto.png" se verdadeiro entao aplicar identificador BlocoComandos fim BlocoComandos
⇒ abrir "foto.png" se verdadeiro entao aplicar brilho BlocoComandos fim BlocoComandos
```

#### 📌 Exemplo de Derivação – Programa com Função
##### Programa:
```
def soma(a, b)
    return a + b
fim
```
```
salvar soma(5, 3)
mostrar "Resultado salvo"
```

### Árvore de Derivação (parcial):
### Programa
```
├── BlocoDeclaracoes
│   └── DeclaracaoFuncao
│       └── def soma ( identificador , identificador ) BlocoComandos fim
│           └── return identificador + identificador
├── BlocoComandos
│   ├── salvar identificador ( literal_inteiro , literal_inteiro )
│   │   └── salvar soma ( 5 , 3 )
│   └── mostrar literal_texto
│       └── mostrar "Resultado salvo"
```

- 👉 Esses dois exemplos já estão no mesmo formato das imagens que você me mandou, só que usando o vocabulário da sua linguagem.

##### 📌 Resolução de Ambiguidades na Linguagem
###### ⚠️ Problemas Identificados e Soluções

1 - Problema do Dangling-Else
```
se condicao1 entao
    se condicao2 entao
        aplicar brilho
senao    # A qual 'se' pertence?
    aplicar contraste
fim
```

✅ Solução:

- Regra de associação: senao sempre se associa ao se mais próximo não pareado.

- Assim, no exemplo acima, o senao está ligado ao segundo se condicao2.

2 - Precedência de Operadores

- Para evitar ambiguidades em expressões, a hierarquia de operadores na linguagem fica definida assim:

- () – Parênteses

- nao – Negação lógica

-  '* / % // ** – Multiplicação, divisão, módulo, divisão inteira e exponenciação

- '+ - – Adição e subtração

- == != > < >= <= – Comparações

- e – AND lógico

- ou – OR lógico

3. Associatividade

- Operadores aritméticos: associativos à esquerda

- Exemplo: 10 - 4 - 2 é interpretado como (10 - 4) - 2

- Operadores lógicos: associativos à esquerda

- Exemplo: verdadeiro e falso ou verdadeiro é interpretado como - ((verdadeiro e falso) ou verdadeiro)

- Comparações: não associativas (erro se encadear sem operadores lógicos)

- ❌ a < b < c → inválido

- ✅ (a < b) e (b < c) → válido

👉 Isso já deixa a sua especificação no mesmo estilo da imagem que você mandou, mas adaptado ao seu alfabeto T.