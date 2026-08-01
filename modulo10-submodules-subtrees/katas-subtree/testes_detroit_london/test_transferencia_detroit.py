from conftest import Conta, Notificador, ServicoTransferencia, ContaInvalidaError

def test_transferencia_atualiza_saldos_detroit():
    origem = Conta(titular="Ana", saldo=100)
    destino = Conta(titular="Bruno", saldo=50)
    servico = ServicoTransferencia(Notificador())

    servico.transferir(origem, destino, 30)

    assert origem.saldo == 70
    assert destino.saldo == 80
