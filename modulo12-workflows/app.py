def saudacao(nome):
    """diz ola para usuario = nome """
    return f"Ola, {nome}!"

def despedida(nome):
    return f"Adeus, {nome}!"

def boas_vindas(nome):
    """funcao corrigida"""
    return f"Bem-vindo(a), {nome}!"

def despedida_formal(nome):
    return f"Atenciosamente, ate breve, {nome}."

FEATURE_LOG_ATIVO = False

def log_acao(acao):
    if FEATURE_LOG_ATIVO:
        print(f"[LOG] {acao}")
