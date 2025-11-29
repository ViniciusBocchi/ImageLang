from ilc.lexer.lexer_afn import LexerAFN
from ilc.parser.parser import parse
from ilc.semantic.semantic_analyzer import analyze
from ilc.codegen.to_python import ToPython
import subprocess, tempfile, os, sys


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__)) 
OUT_DIR = os.path.join(PROJECT_ROOT, "out")                


def compile_file(src_path, output_name):
    with open(src_path, 'r', encoding='utf-8') as f:
        src = f.read()

    # Pipeline: Lexer -> Parser -> Semantic -> Codegen
    lexer = LexerAFN(src)
    tokens = lexer.tokenize()
    ast = parse(tokens)
    
    analyze(ast)
    python_code = ToPython(ast).generate()

    python_code = ToPython(ast).generate()

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, output_name)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(python_code)

    print(f"[OK] Arquivo gerado em: {out_path}")


def execute_file(src_path):
    fd, tmp = tempfile.mkstemp(suffix='.py')
    os.close(fd)

    try:
        compile_file(src_path, os.path.basename(tmp))
        ret = subprocess.run([sys.executable, tmp])
        if ret.returncode != 0:
            raise SystemExit(ret.returncode)
    finally:
        try:
            os.remove(tmp)
        except:
            pass
