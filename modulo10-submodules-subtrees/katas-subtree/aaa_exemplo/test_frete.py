import pytest
from frete import calcular_frete

def test_calcular_frete_peso_zero_ou_negativo_levanta_valueerror():
    # Arrange: nao precisa de setup, os valores ja sao o cenario
    # Act + Assert: aqui as duas etapas se fundem - isso e normal
    # quando o comportamento esperado e uma excecao, nao um retorno
    with pytest.raises(ValueError):
        calcular_frete(peso_kg=0, distancia_km=10)

def test_frete_gratis_caso_peso_menos_que_5kg_e_distancia_menos_50km():
    assert calcular_frete(peso_kg=4, distancia_km=40) == 0


def test_frete_normal_calcula_peso_vezes_2_mais_distancia_vezes_0_5():
    assert calcular_frete(peso_kg=10, distancia_km=20) == 30


def test_frete_normal_caso_peso_menos_que_5_distancia_maior_que_50():
    assert calcular_frete(peso_kg=3, distancia_km=100) == 56
