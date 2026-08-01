class ContaInvalidaError(Exception):
    pass

class Notificador:
    def enviar(self, destinatario, mensagem):
        # em produção, chamaria uma API externa
        pass

class ServicoTransferencia:
    def __init__(self, notificador):
        self.notificador = notificador

    def transferir(self, origem, destino, valor):
        if origem.saldo < valor:
            raise ContaInvalidaError("Saldo insuficiente")
        origem.saldo -= valor
        destino.saldo += valor
        self.notificador.enviar(destino.titular, f"Você recebeu R${valor}")

class Conta:
    def __init__(self, titular, saldo):
        self.titular = titular
        self.saldo = saldo
