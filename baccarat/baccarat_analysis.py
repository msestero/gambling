from .baccarat import Baccarat

import pandas as pd
import matplotlib.pyplot as plt

def main():
    # hands_per_hour = 72
    # hours_spent = 4000
    # tot = hands_per_hour * hours_spent
    tot = 100000
    game = Baccarat()
    high = 0
    low = 0
    drops = []
    results = game.play(tot)
    #pd.Series(results).plot.line()
    #plt.show()
    for result in results:
        if result > high and high != low:
            drops.append(high - low)
        if result > high:
            high = result
            low = result
        if result < low:
            low = result
    drops.append(high - low)
    # pd.Series(drops).plot.hist()
    # plt.show()
    pd.Series(results).plot.line()
    plt.show()
    print(pd.Series(drops).max())
    print(pd.Series(drops).mean())
    print(results[len(results) - 1] / tot)
    print(pd.Series(results).min())
    print(results[len(results) - 1])


if __name__ == "__main__":
    main()