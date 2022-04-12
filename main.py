from poker import game
from poker import player

if __name__ == "__main__":
    game = game(1000, 5, 50)
    player1 = player("player1", 1000)
    player2 = player("player2", 1000)
    player3 = player("player3", 1000)
    game.addPlayer(player1, 0)
    game.addPlayer(player2, 1)
    game.addPlayer(player3, 8)
    game.play_round()