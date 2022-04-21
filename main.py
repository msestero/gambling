from blackjack import BlackJack
from blackjack import Player
from blackjack import BasicStrategyPlayer

def main():
    tot_hands = 0
    attempts = 1000
    starting_cash = 1000
    for i in range(attempts):
        player = BasicStrategyPlayer(starting_cash)
        game = BlackJack(player, decks=6, show_terminal=False)
        tot_hands += game.play()
    average_hands = tot_hands / attempts
    if average_hands > 0:
        average_loss_per = starting_cash / average_hands
    else:
        average_loss_per = 0
    edge = average_loss_per / 25 * 100
    print("average num hands : {:.2f}".format(average_hands))
    print("average loss: ${:.2f}".format(average_loss_per))
    print("house edge: {:.2f}%".format(edge))

if __name__ == "__main__":
    main()