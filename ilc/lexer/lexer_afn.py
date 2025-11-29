from dataclasses import dataclass
from typing import List
from ilc.runtime.buffer_otimizado import BufferOtimizado 

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
    # IO
    'abrir_imagem', 'salvar_imagem',
        
    # Conectores da linguagem
    'como', 'para', 'por', 'filtro', 'raio', 'texto', 'em', 'tamanho',
    'cor', 'espessura', 'com', 'alpha',

    # Controle
    'salvar', 'loop', 'cada', 'arquivo', 'executar',

    # Transformações geométricas
    'rotacionar', 'redimensionar', 'cortar', 'transladar', 'espelhar',
    'warp_perspectiva', 'remap',

    # Filtros e denoise
    'aplicar_filtro', 'desfocar', 'mediana', 'bilateral', 'remover_ruido',

    # Ajustes
    'ajustar_brilho_contraste', 'ajustar_gamma', 'gamma', 'clahe',

    # Canais e cores
    'converter_canal', 'bgr_to_rgb', 'rgb_to_bgr', 'converter_para_gray',

    # Bordas e detecção
    'detectar_bordas', 'detectar_contornos', 'desenhar_contornos',
    'detectar_circulos', 'detectar_retangulos',

    # Morfologia
    'morfologia', 'erodir', 'dilatar', 'abrir_morf', 'fechar_morf',

    # Equalização e histograma
    'equalizar_histograma', 'equalizar_color', 'histograma', 'equalizar_clahe',

    # Segmentação
    'thresholding', 'kmeans_segmentacao', 'grabcut_remover_fundo',

    # Efeitos artísticos
    'cartoonize', 'pencil_sketch', 'oil_painting',

    # Faces
    'detectar_faces', 'desenhar_bbox',

    # Blending
    'alpha_blend', 'overlay_image', 'overlay_text',

    # Utilitários
    'resize_max', 'ensure_color', 'to_bytes'
}


class LexerAFN:
    def __init__(self, arquivo_binario=None):
        if arquivo_binario is None:
            arquivo_binario = ""

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

            if c.isspace():
                self.advance()
                continue

            if c == '/' and chr(self.peek(1)) == '/':
                while True:
                    if self.advance() == -1 or chr(self.peek()) == '\n':
                        break
                self.advance()
                continue

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

            if c in SINGLE_CHAR_TOKENS:
                tokens.append(Token(SINGLE_CHAR_TOKENS[c], c, self.line, self.col))
                self.advance()
                continue

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

            tokens.append(Token('SYMBOL', c, self.line, self.col))
            self.advance()

        tokens.append(Token('EOF', '', self.line, self.col))
        return tokens
