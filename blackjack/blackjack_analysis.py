from .blackjack import BlackJack
from .blackjack import Player
from .blackjack import BasicStrategyPlayer
from .blackjack import CardCounter

import pandas as pd
import matplotlib.pyplot as plt
from numpy import transpose

from time import process_time

def sim_game():
    starting_cash = 0
    spread = 20
    max_hands = 1000000
    #player = BasicStrategyPlayer(starting_cash, max_hands)
    player = CardCounter(starting_cash, max_hands, spread)
    game = BlackJack(player, min_bet=5, decks=6, show_terminal=False)
    return game.play()


def main():
    attempts = 1
    t = process_time()
    games = []
    while len(games) < attempts:
        games.append(sim_game())
    print("time:", process_time() - t)
    df_money = get_df_money(games)
    plot_money(df_money)
    print(ev_per_hand(df_money))
    print(calc_edge(df_money))
    print(df_money.min())


def get_df_money(games):
    moneys = list(map(lambda y : list(map(lambda x : x.money, y)), games))
    return pd.DataFrame(moneys).T

def plot_money(df_money):
    df_money.plot.line()
    plt.show()

def ev_per_hand(df_money):
    totals = df_money.sum(axis=1)
    tot_ret = totals[totals.size - 1]
    return tot_ret / (len(df_money.columns) * len(df_money.index - 1))

def calc_edge(df_money, min_bet=25):
    return (ev_per_hand(df_money) / min_bet) * 100

    
if __name__ == "__main__":
    main()