from conftest import Conta, Notificador, ServicoTransferencia, ContaInvalidaError

def test_transferencia_notifica_destino_london(mocker):
    origem = Conta(titular="Ana", saldo=100)
    destino = Conta(titular="Bruno", saldo=50)
    notificador_mock = mocker.Mock()
    servico = ServicoTransferencia(notificador_mock)

    servico.transferir(origem, destino, 30)

    notificador_mock.enviar.assert_called_once_with("Bruno", "Você recebeu R$30")
