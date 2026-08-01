from fizzbuzz import fizzbuzz


def test_fizzbuzz_retorna_numero_quando_nao_multiplo():
    assert fizzbuzz(1) == "1"

def test_fizzbuzz_retorna_fizz_quando_multiplo_de_3():
    assert fizzbuzz(3) == "Fizz"

def test_fizzbuzz_retorna_buzz_quando_multiplo_de_5():
    assert fizzbuzz(5) == "Buzz"
def test_fizzbuzz_retorna_fizzbuzz_quando_multiplo_de_ambos():
    assert fizzbuzz(15) == "FizzBuzz"
