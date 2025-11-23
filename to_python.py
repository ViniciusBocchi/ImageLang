from ilc.parser.parser import ASTNode

def generate_python(ast: ASTNode) -> str:
    header = [
        '# Auto-gerado por ImageLang',
        'import sys, os',
        'sys.path.append(os.path.dirname(os.path.dirname(__file__)))',
        'from ilc.runtime.il_runtime import *',
        ''
    ]
    body = ['def main():']
    for s in ast.statements:
        if s.type == 'Abrir':
            body.append(f"    {s.id} = abrir_imagem(r'''{s.path}''')")
        elif s.type == 'Salvar':
            body.append(f"    salvar_imagem({s.id}, r'''{s.path}''')")
        elif s.type == 'Rotacionar':
            body.append(f"    {s.dst} = rotacionar({s.src}, {s.graus})")
        elif s.type == 'Redimensionar':
            body.append(f"    {s.dst} = redimensionar({s.src}, {s.w}, {s.h})")
        elif s.type == 'Cortar':
            body.append(f"    {s.dst} = cortar({s.src}, {s.x}, {s.y}, {s.w}, {s.h})")
        elif s.type == 'AplicarFiltro':
            if s.raio is None:
                body.append(f"    {s.dst} = aplicar_filtro({s.src}, r'''{s.filtro}''')")
            else:
                body.append(f"    {s.dst} = aplicar_filtro({s.src}, r'''{s.filtro}''', raio={s.raio})")
        elif s.type == 'AdicionarTexto':
            r,g,b = s.cor
            body.append(f"    adicionar_texto({s.src}, r'''{s.texto}''', {s.x}, {s.y}, {s.tamanho}, ({r},{g},{b}), {s.espessura})")
    footer = ["","if __name__ == '__main__':","    main()",""]
    return '\n'.join(header + body + footer)
