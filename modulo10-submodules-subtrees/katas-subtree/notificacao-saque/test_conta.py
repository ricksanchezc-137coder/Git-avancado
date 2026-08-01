from unittest.mock import Mock
from conta import Conta
def test_saque_normal_nao_notifica():
    notificador_mock = Mock()
    conta = Conta(saldo=1000, notificador=notificador_mock)
    conta.sacar(200)
    assert conta.saldo == 800
    notificador_mock.enviar.assert_not_called() 

def test_saque_alto_dispara_notificador():
    notificador_mock = Mock()
    conta = Conta(saldo=1000, notificador=notificador_mock)
    conta.sacar(600)

    notificador_mock.enviar.assert_called_once_with(
        "saque de alto valor: 600"
    )

def test_saldo_insuficiente_nao_saca_nem_notifica():
    notificador_mock = Mock()
    conta= Conta(saldo=1000, notificador=notificador_mock)
    with pytest.raises(ValueError):
        conta.sacar(1500)
    assert conta.saldo == 1000
    notificador_mock.enviar.assert_not_called()

import pytest
