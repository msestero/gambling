from blackjack import BlackJack
from blackjack import Player
from blackjack import BasicStrategyPlayer

def main():
    tot_hands = 0
    attempts = 10000
    starting_cash = 1000
    for i in range(attempts):
        player = BasicStrategyPlayer(starting_cash)
        game = BlackJack(player, decks=1)
        tot_hands += game.play()
    average_hands = tot_hands / attempts
    average_loss_per = starting_cash / average_hands
    edge = average_loss_per / 25
    print(average_hands, average_loss_per, edge)

if __name__ == "__main__":
    main()