
from unittest.mock import Mock
from servico_transferencia import ServicoTransferencia


# --- DUMMY ---
# Passamos algo só pra satisfazer o parâmetro, nunca é chamado nesse teste
def test_dummy_notificador_nao_usado():
    class RepositorioStub:
        def buscar_saldo(self, conta): return 0

    dummy_notificador = None  # nunca vai ser chamado, pois saldo é insuficiente
    servico = ServicoTransferencia(RepositorioStub(), dummy_notificador)
    resultado = servico.transferir("A", "B", 100)
    assert resultado["sucesso"] is False


# --- STUB ---
# Só devolve uma resposta enlatada. Verificamos o ESTADO do resultado.
def test_stub_saldo_insuficiente():
    class RepositorioStub:
        def buscar_saldo(self, conta): return 50  # sempre 50, fixo

    servico = ServicoTransferencia(RepositorioStub(), notificador=None)
    resultado = servico.transferir("A", "B", 100)
    assert resultado["sucesso"] is False
    assert resultado["motivo"] == "saldo insuficiente"


# --- SPY ---
# Grava as chamadas recebidas. Verificamos DEPOIS se foi chamado certo.
def test_spy_notificador_foi_chamado():
    class RepositorioStub:
        def buscar_saldo(self, conta): return 500
        def debitar(self, conta, valor): pass
        def creditar(self, conta, valor): pass

    class NotificadorSpy:
        def __init__(self):
            self.chamadas = []
        def enviar(self, destino, mensagem):
            self.chamadas.append((destino, mensagem))

    spy = NotificadorSpy()
    servico = ServicoTransferencia(RepositorioStub(), spy)
    servico.transferir("A", "B", 100)

    assert len(spy.chamadas) == 1
    assert spy.chamadas[0][0] == "B"


# --- MOCK ---
# Declaramos a expectativa ANTES, e o próprio mock cobra se não cumprir.
def test_mock_notificador_chamado_com_argumentos_certos(mocker):
    repositorio_stub = mocker.Mock()
    repositorio_stub.buscar_saldo.return_value = 500

    notificador_mock = mocker.Mock()
    servico = ServicoTransferencia(repositorio_stub, notificador_mock)
    servico.transferir("A", "B", 100)

    notificador_mock.enviar.assert_called_once_with("B", "Você recebeu R$ 100")


# --- FAKE ---
# Implementação real e funcional, só que simplificada (dicionário em vez de SQLite)
class RepositorioFake:
    def __init__(self):
        self._saldos = {"A": 500, "B": 0}
    def buscar_saldo(self, conta): return self._saldos[conta]
    def debitar(self, conta, valor): self._saldos[conta] -= valor
    def creditar(self, conta, valor): self._saldos[conta] += valor

def test_fake_repositorio_atualiza_saldos_de_verdade():
    fake = RepositorioFake()
    notificador_stub = Mock()
    servico = ServicoTransferencia(fake, notificador_stub)
    servico.transferir("A", "B", 100)

    assert fake.buscar_saldo("A") == 400
    assert fake.buscar_saldo("B") == 100
