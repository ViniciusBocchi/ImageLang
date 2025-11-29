
import os
import pytest
from ilc.frontend import compile_file

blocos = [
    '''abrir_imagem "foto.jpg" como img1;
    alpha_blend img1 com img1 alpha 0.5 como img2;
    overlay_image img2 com img1 em 10,10 alpha 0.8 como img3;
    overlay_text img3 texto "Texto" em 100,100 tamanho 1.0 cor 255,255,255 espessura 2 como img4;'''
]

@pytest.mark.parametrize('codigo', blocos)
def test_blocos(codigo, tmp_path):
    il_file = tmp_path / 'teste.il'
    py_file = tmp_path / 'saida.py'
    il_file.write_text(codigo, encoding='utf-8')
    compile_file(str(il_file), str(py_file))
    conteudo = py_file.read_text(encoding='utf-8')
    assert 'def main' in conteudo
