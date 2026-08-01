class BowLingGame:
    def __init__(self):
        self._jogadas = []

    def rolar(self, pinos):
        self._jogadas.append(pinos)

    def pontuacao(self):
        total = 0
        i = 0
        for _ in range(10):
            if self._eh_strike(i):
                total += 10 + self._bonus_strike(i)
                i += 1
            elif self._eh_spare(i):
                total += 10 + self._bonus_spare(i)
                i += 2
            else:
                total += self._pontos_frame_simples(i)
                i += 2
        return total

    def _eh_strike(self, i):
        return self._jogadas[i] == 10

    def _eh_spare(self, i):
        return self._jogadas[i] + self._jogadas[i + 1] == 10

    def _bonus_strike(self, i):
        return self._jogadas[i + 1] + self._jogadas[i + 2]

    def _bonus_spare(self, i):
        return self._jogadas[i + 2]

    def _pontos_frame_simples(self, i):
        return self._jogadas[i] + self._jogadas[i + 1]
