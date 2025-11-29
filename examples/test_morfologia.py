
import os
import pytest
from ilc.frontend import compile_file

blocos = [
    '''abrir_imagem "foto.jpg" como img1;
    erodir img1 ksize 3 como img2;
    dilatar img2 ksize 3 como img3;
    abrir_morf img3 ksize 3 como img4;
    fechar_morf img4 ksize 3 como img5;'''
]

@pytest.mark.parametrize('codigo', blocos)
def test_blocos(codigo, tmp_path):
    il_file = tmp_path / 'teste.il'
    py_file = tmp_path / 'saida.py'
    il_file.write_text(codigo, encoding='utf-8')
    compile_file(str(il_file), str(py_file))
    conteudo = py_file.read_text(encoding='utf-8')
    assert 'def main' in conteudo
