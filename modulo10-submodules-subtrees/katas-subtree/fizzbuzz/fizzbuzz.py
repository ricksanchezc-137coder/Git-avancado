def fizzbuzz(numero):
    resultado = ""
    if numero % 3 == 0:
        resultado += "Fizz"
    if numero % 5 == 0:
        resultado += "Buzz"
    return resultado or str(numero)
