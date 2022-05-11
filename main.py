from blackjack import BlackJack
from blackjack import Player
from blackjack import BasicStrategyPlayer

import pandas as pd
import matplotlib.pyplot as plt
from numpy import transpose

def main():
    attempts = 1
    starting_cash = 10000
    games = []
    for i in range(attempts):
        player = BasicStrategyPlayer(starting_cash)
        game = BlackJack(player, decks=6, show_terminal=True)
        games.append(game.play())
    moneys = list(map(lambda y : (list(map(lambda x : x.money, y))), games))
    pd.DataFrame(moneys).T.plot.line()
    plt.show()

if __name__ == "__main__":
    main()