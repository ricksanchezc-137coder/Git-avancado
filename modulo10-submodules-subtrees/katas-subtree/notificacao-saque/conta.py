class Conta:
    LIMITE_NOTIFICACAO=500
    def __init__(self, saldo, notificador):
        self.saldo = saldo
        self.notificador = notificador
    def sacar(self, valor):
        if valor > self.saldo:
            raise ValueError("saldo insuficiente")

        self.saldo -= valor
        if valor > self.LIMITE_NOTIFICACAO:
            self.notificador.enviar(f"saque de alto valor: {valor}")
