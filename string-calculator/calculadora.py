def _extrair_delimitador_e_corpo(numeros):
    if numeros.startswith("//"):
        fim_cabecalho = numeros.index("\n")
        delimitador = numeros[2:fim_cabecalho]
        corpo = numeros[fim_cabecalho + 1:]
        return delimitador, corpo
    return ",", numeros


def _validar_negativos(valores):
    negativos = [v for v in valores if v < 0]
    if negativos:
        raise ValueError(f"numeros negativos nao permitidos: {negativos}")


def somar(numeros):
    if numeros == "":
        return 0

    delimitador, corpo = _extrair_delimitador_e_corpo(numeros)
    corpo = corpo.replace("\n", ",")
    partes = corpo.split(delimitador)
    valores = [int(p) for p in partes]

    _validar_negativos(valores)

    return sum(valores)
