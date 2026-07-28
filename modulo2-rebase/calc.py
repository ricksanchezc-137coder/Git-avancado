# Caculadora
def soma(a, b):
    return a + b

def subtrai(a, b):
    return a - b

def multiplica(a, b):
    """Multiplica dois numeros"""
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Divisao por zero")
    return a / b

