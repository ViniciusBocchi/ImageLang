"""
Lexer com Buffer Duplo Otimizado
Suporte a:
 - Identificadores
 - Números
 - Strings
 - Comentários
 - Palavras-chave e símbolos
"""

from dataclasses import dataclass
from typing import List
from ilc.runtime.il_runtime import BufferOtimizado  # ✅ IMPORT DO BUFFER

@dataclass
class Token:
    type: str
    value: str
    line: int
    col: int
    def __repr__(self):
        return f"Token({self.type!r},{self.value!r},{self.line},{self.col})"


SINGLE_CHAR_TOKENS = {
    ';': 'SEMICOLON',
    ',': 'COMMA',
    '{': 'LBRACE',
    '}': 'RBRACE',
    '(' : 'LPAREN',
    ')' : 'RPAREN',
    'x': 'SYMBOL',
    'X': 'SYMBOL'
}

KEYWORDS = {
    'abrir_imagem', 'salvar_imagem', 'como', 'rotacionar', 'por', 'redimensionar', 'para',
    'cortar', 'aplicar_filtro', 'filtro', 'raio', 'adicionar_texto', 'texto', 'em',
    'tamanho', 'cor', 'espessura', 'sobrepor', 'com', 'alpha', 'salvar', 'loop',
    'cada', 'arquivo', 'executar'
}


# -------------------------------
# Lexer principal
# -------------------------------

class LexerAFN:
    def __init__(self, arquivo_binario):
        self.buffer = BufferOtimizado(arquivo_binario)
        self.line = 1
        self.col = 1

    def advance(self):
        char = self.buffer.proximo_caractere()
        if char == -1:
            return -1
        c = chr(char)

        if c == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        
        return char

    def peek(self, offset=0):
        return self.buffer.espiar_caractere(offset)

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []

        while True:
            char = self.peek()
            if char == -1:
                break

            c = chr(char)

            # Ignorar espaços e quebras
            if c.isspace():
                self.advance()
                continue

            # Comentários tipo //
            if c == '/' and chr(self.peek(1)) == '/':
                while True:
                    if self.advance() == -1 or chr(self.peek()) == '\n':
                        break
                self.advance()
                continue

            # Strings
            if c == '"':
                start_col = self.col
                self.advance()
                val = []
                while True:
                    ch = self.peek()
                    if ch == -1:
                        break
                    c2 = chr(ch)
                    if c2 == '"':
                        self.advance()
                        break
                    val.append(c2)
                    self.advance()
                tokens.append(Token('STRING', ''.join(val), self.line, start_col))
                continue

            # Símbolos simples
            if c in SINGLE_CHAR_TOKENS:
                tokens.append(Token(SINGLE_CHAR_TOKENS[c], c, self.line, self.col))
                self.advance()
                continue

            # Números
            if c.isdigit():
                start_col = self.col
                val = []
                while chr(self.peek()).isdigit():
                    val.append(chr(self.advance()))
                if chr(self.peek()) == '.':
                    val.append(chr(self.advance()))
                    while chr(self.peek()).isdigit():
                        val.append(chr(self.advance()))
                tokens.append(Token('NUMBER', ''.join(val), self.line, start_col))
                continue

            # Identificadores
            if c.isalpha() or c == '_':
                start_col = self.col
                val = []
                while True:
                    ch = self.peek()
                    if ch == -1:
                        break
                    c2 = chr(ch)
                    if not (c2.isalnum() or c2 in ['_', '-']):
                        break
                    val.append(c2)
                    self.advance()
                ident = ''.join(val)
                if ident in KEYWORDS:
                    tokens.append(Token(ident.upper(), ident, self.line, start_col))
                else:
                    tokens.append(Token('IDENT', ident, self.line, start_col))
                continue

            # Qualquer outro caractere
            tokens.append(Token('SYMBOL', c, self.line, self.col))
            self.advance()

        tokens.append(Token('EOF', '', self.line, self.col))
        return tokens
