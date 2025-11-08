from typing import Any

class ASTNode:
    def __init__(self, type: str, **kwargs: Any):
        self.type = type
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        attrs = {k: v for k, v in self.__dict__.items() if k != 'type'}
        return f"ASTNode({self.type}, {attrs})"


class ParserError(Exception):
    pass


class TokenProxy:
    def __init__(self, t):
        self.type = t.type
        self.value = t.value
        self.line = t.line
        self.col = t.col

    def __repr__(self):
        return f"Token({self.type},{self.value})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
        self.cur = TokenProxy(tokens[0])

    def advance(self):
        self.i += 1
        if self.i < len(self.tokens):
            self.cur = TokenProxy(self.tokens[self.i])

    def eat(self, *expected):
        for e in expected:
            if self.cur.type == e or self.cur.value == e:
                tok = self.cur
                self.advance()
                return tok
        raise ParserError(f"Esperado {expected}, encontrado {self.cur}")

    def parse(self):
        stmts = []
        while self.cur.type != 'EOF':
            if self.cur.type == 'ABRIR_IMAGEM':
                stmts.append(self.parse_abrir())
            elif self.cur.type == 'SALVAR_IMAGEM':
                stmts.append(self.parse_salvar())
            elif self.cur.type == 'ROTACIONAR':
                stmts.append(self.parse_rotacionar())
            elif self.cur.type == 'REDIMENSIONAR':
                stmts.append(self.parse_redimensionar())
            elif self.cur.type == 'CORTAR':
                stmts.append(self.parse_cortar())
            elif self.cur.type == 'APLICAR_FILTRO':
                stmts.append(self.parse_aplicar_filtro())
            elif self.cur.type == 'ADICIONAR_TEXTO':
                stmts.append(self.parse_adicionar_texto())
            elif self.cur.type == 'SOBREPOR':
                stmts.append(self.parse_sobrepor())
            else:
                raise ParserError(f"Comando desconhecido: {self.cur}")
        return ASTNode('Program', statements=stmts)

    def parse_abrir(self):
        self.eat('ABRIR_IMAGEM')
        s = self.eat('STRING')
        self.eat('COMO', 'como')
        idt = self.eat('IDENT')
        self.eat('SEMICOLON', ';')
        return ASTNode('Abrir', path=s.value, id=idt.value)

    def parse_salvar(self):
        self.eat('SALVAR_IMAGEM')
        idt = self.eat('IDENT')
        if self.cur.type == 'EM' or self.cur.value == 'em':
            self.eat(self.cur.type)
        s = self.eat('STRING')
        self.eat('SEMICOLON', ';')
        return ASTNode('Salvar', id=idt.value, path=s.value)

    def parse_rotacionar(self):
        self.eat('ROTACIONAR')
        src = self.eat('IDENT')
        self.eat('POR', 'por')
        num = self.eat('NUMBER')
        self.eat('COMO', 'como')
        dst = self.eat('IDENT')
        self.eat('SEMICOLON', ';')
        return ASTNode('Rotacionar', src=src.value, graus=float(num.value), dst=dst.value)

    def parse_redimensionar(self):
        self.eat('REDIMENSIONAR')
        src = self.eat('IDENT')
        self.eat('PARA', 'para')
        w = self.eat('NUMBER')
        if self.cur.type == 'SYMBOL' and self.cur.value.lower() == 'x':
            self.eat('SYMBOL')
        else:
            self.eat('SYMBOL', 'x', 'X')
        h = self.eat('NUMBER')
        self.eat('COMO', 'como')
        dst = self.eat('IDENT')
        self.eat('SEMICOLON', ';')
        return ASTNode('Redimensionar', src=src.value, w=int(w.value), h=int(h.value), dst=dst.value)

    def parse_cortar(self):
        self.eat('CORTAR')
        src = self.eat('IDENT')
        self.eat('PARA', 'para')
        x = self.eat('NUMBER'); self.eat('COMMA', ',')
        y = self.eat('NUMBER'); self.eat('COMMA', ',')
        w = self.eat('NUMBER'); self.eat('COMMA', ',')
        h = self.eat('NUMBER')
        self.eat('COMO', 'como')
        dst = self.eat('IDENT')
        self.eat('SEMICOLON', ';')
        return ASTNode('Cortar', src=src.value, x=int(x.value), y=int(y.value), w=int(w.value), h=int(h.value), dst=dst.value)

    def parse_aplicar_filtro(self):
        self.eat('APLICAR_FILTRO')
        src = self.eat('IDENT')
        self.eat('FILTRO', 'filtro')
        nome = self.eat('STRING')
        raio = None
        if self.cur.type == 'RAIO' or self.cur.value == 'raio':
            self.eat(self.cur.type)
            raio_tok = self.eat('NUMBER')
            raio = int(raio_tok.value)
        self.eat('COMO', 'como')
        dst = self.eat('IDENT')
        self.eat('SEMICOLON', ';')
        return ASTNode('AplicarFiltro', src=src.value, filtro=nome.value, raio=raio, dst=dst.value)

    def parse_adicionar_texto(self):
        self.eat('ADICIONAR_TEXTO')
        src = self.eat('IDENT')
        self.eat('TEXTO', 'texto')
        txt = self.eat('STRING')
        self.eat('EM', 'em')
        x = self.eat('NUMBER'); self.eat('COMMA', ',')
        y = self.eat('NUMBER')
        self.eat('TAMANHO', 'tamanho')
        t = self.eat('NUMBER')
        self.eat('COR', 'cor')
        r = self.eat('NUMBER'); self.eat('COMMA', ',')
        g = self.eat('NUMBER'); self.eat('COMMA', ',')
        b = self.eat('NUMBER')
        self.eat('ESPESSURA', 'espessura')
        e = self.eat('NUMBER')
        self.eat('SEMICOLON', ';')
        return ASTNode('AdicionarTexto',
                       src=src.value,
                       texto=txt.value,
                       x=int(x.value),
                       y=int(y.value),
                       tamanho=int(t.value),
                       cor=(int(r.value), int(g.value), int(b.value)),
                       espessura=int(e.value))

    def parse_sobrepor(self):
        self.eat('SOBREPOR')
        base = self.eat('IDENT')
        if self.cur.type == 'COM' or self.cur.value == 'com':
            self.eat(self.cur.type)
        overlay = self.eat('IDENT')
        if self.cur.type == 'EM' or self.cur.value == 'em':
            self.eat(self.cur.type)
        x = self.eat('NUMBER'); self.eat('COMMA', ',')
        y = self.eat('NUMBER')
        if self.cur.type == 'ALPHA' or self.cur.value == 'alpha':
            self.eat(self.cur.type)
        a = self.eat('NUMBER')
        self.eat('COMO', 'como')
        dst = self.eat('IDENT')
        self.eat('SEMICOLON', ';')
        return ASTNode('Sobrepor', base=base.value, overlay=overlay.value, x=int(x.value), y=int(y.value), alpha=float(a.value), dst=dst.value)


def parse(tokens):
    p = Parser(tokens)
    return p.parse()
