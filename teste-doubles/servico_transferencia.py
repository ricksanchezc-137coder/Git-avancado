
class ServicoTransferencia:
    def __init__(self, repositorio, notificador):
        self.repositorio = repositorio
        self.notificador = notificador

    def transferir(self, origem, destino, valor):
        saldo = self.repositorio.buscar_saldo(origem)
        if saldo < valor:
            return {"sucesso": False, "motivo": "saldo insuficiente"}

        self.repositorio.debitar(origem, valor)
        self.repositorio.creditar(destino, valor)
        self.notificador.enviar(destino, f"Você recebeu R$ {valor}")
        return {"sucesso": True}
