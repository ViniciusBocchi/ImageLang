from ilc.parser.parser import ASTNode

class SemanticError(Exception): pass

def analyze(ast: ASTNode):
    defined = set()
    for s in ast.statements:
        t = s.type
        if t == 'Abrir':
            defined.add(s.id)
        elif t in ('Rotacionar','Redimensionar','Cortar','AplicarFiltro'):
            if not hasattr(s, 'src') or s.src not in defined:
                raise SemanticError(f"Uso de variável não definida: {getattr(s,'src',None)}")
            defined.add(s.dst)
        elif t == 'Salvar':
            if s.id not in defined:
                raise SemanticError(f"Salvar: variável não definida: {s.id}")
        elif t == 'AdicionarTexto':
            if s.src not in defined:
                raise SemanticError(f"AdicionarTexto: variável não definida: {s.src}")
        elif t == 'Sobrepor':
            if s.base not in defined or s.overlay not in defined:
                raise SemanticError(f"Sobrepor: variáveis não definidas: {s.base},{s.overlay}")
            defined.add(s.dst)
    return True
