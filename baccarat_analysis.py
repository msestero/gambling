from baccarat import Baccarat

import pandas as pd
import matplotlib.pyplot as plt

def main():
    tot = 10000000
    game = Baccarat()
    results = game.play(tot)
    #pd.Series(results).plot.line()
    #plt.show()
    print(results[len(results) - 1] / tot)
    print(pd.Series(results).min())
    print(results[len(results) - 1])


if __name__ == "__main__":
    main()