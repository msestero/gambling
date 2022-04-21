from blackjack import BlackJack
from blackjack import Player
from blackjack import BasicStrategyPlayer

def main():
    attempts = 100
    starting_cash = 1000
    tot_high = starting_cash
    for i in range(attempts):
        player = BasicStrategyPlayer(starting_cash)
        game = BlackJack(player, decks=1, show_terminal=False)
        tot_high += game.play()
    print(tot_high / attempts)

if __name__ == "__main__":
    main()