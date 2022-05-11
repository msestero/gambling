from blackjack import BlackJack
from blackjack import Player
from blackjack import BasicStrategyPlayer
from blackjack import CardCounter

import pandas as pd
import matplotlib.pyplot as plt
from numpy import transpose

def main():
    attempts = 100
    starting_cash = 100000
    spread = 30
    max_hands = 10000
    games = []
    for i in range(attempts):
        player = CardCounter(starting_cash, max_hands, spread)
        game = BlackJack(player, min_bet=5, decks=6, show_terminal=True)
        games.append(game.play())
    moneys = list(map(lambda y : list(map(lambda x : x.money, y)), games))
    pd.DataFrame(moneys).T.plot.line()
    plt.show()

if __name__ == "__main__":
    main()