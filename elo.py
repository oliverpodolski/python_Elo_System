class EloCalculator:

    def calculate(self, winner_elo, loser_elo, k_factor=30):

        expected_winner = 1 / (1+ 10 ** ((loser_elo - winner_elo) / 400))

        elo_change = round(k_factor * (1 - expected_winner))

        return elo_change

