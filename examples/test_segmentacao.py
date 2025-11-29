
import os
import pytest
from ilc.frontend import compile_file

blocos = [
    '''abrir_imagem "foto.jpg" como img1;
    thresholding img1 metodo "binary" thresh 127 tipo "binary" como img2;
    kmeans_segmentacao img2 k 3 como img3;
    grabcut_remover_fundo img3 rect 0,0,100,100 iter 5 como img4;'''
]

@pytest.mark.parametrize('codigo', blocos)
def test_blocos(codigo, tmp_path):
    il_file = tmp_path / 'teste.il'
    py_file = tmp_path / 'saida.py'
    il_file.write_text(codigo, encoding='utf-8')
    compile_file(str(il_file), str(py_file))
    conteudo = py_file.read_text(encoding='utf-8')
    assert 'def main' in conteudo
