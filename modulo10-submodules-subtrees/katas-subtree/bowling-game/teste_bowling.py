import pytest
from bowling import BowLingGame


class TestBowLingGame:
    def test_jogo_todo_zero_pontua_zero(self):
        jogo = BowLingGame()
        for _ in range(20):
            jogo.rolar(0)
        assert jogo.pontuacao() == 0

    def test_jogo_todo_com_um_pontua_vinte(self):
        jogo = BowLingGame()
        for _ in range(20):
            jogo.rolar(1)
        assert jogo.pontuacao() == 20

    def test_um_spare_soma_bonus_da_proxima_jogada(self):
        jogo = BowLingGame()
        jogo.rolar(5)
        jogo.rolar(5)
        jogo.rolar(3)
        for _ in range(17):
            jogo.rolar(0)
        assert jogo.pontuacao() == 16

    def test_um_strike_soma_bonus_das_proximas_duas_jogadas(self):
        jogo = BowLingGame()
        jogo.rolar(10)
        jogo.rolar(3)
        jogo.rolar(4)
        for _ in range(16):
            jogo.rolar(0)
        assert jogo.pontuacao() == 24

    def test_jogo_perfeito_pontua_trezentos(self):
        jogo = BowLingGame()
        for _ in range(12):
            jogo.rolar(10)
        assert jogo.pontuacao() == 300
