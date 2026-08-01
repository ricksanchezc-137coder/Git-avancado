from calculadora import somar

def test_string_vazio_retorna_zero():
    assert somar("") == 0

def test_um_numero_retorna_o_propio_valor():
    assert somar("1") == 1

def test_dois_numeros_retorna_soma():
    assert somar("1,2") == 3

def test_varios_numeros_retorna_soma():
    assert somar("1,2,3,4,5") == 15

def test_aceita_quebra_de_linha_como_separador():
    assert somar("1\n2,3") == 6

def test_aceita_delimitador_customizado():
    assert somar("//;\n1;2") == 3

import pytest

def test_numero_negativo_lanca_excecao():
    with pytest.raises(ValueError) as erro:
        somar("1,-2,3")
    assert "-2" in str(erro.value)
