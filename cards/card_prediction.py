from .deck import Deck
from .deck import PokerCard
from random import randint
from time import sleep

# first neural network with keras tutorial
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN

import pandas as pd

from sklearn.preprocessing import MinMaxScaler

def create_decks(decks, iters):
    data = []
    deck = Deck(PokerCard, num_decks=decks)
    for i in range(iters):
        info = []
        for i in range(52 * decks):
            info.append(deck.deal())
        data.append(info)
        deck.shuffle()
    return pd.DataFrame(data)

def edit_y_suites(x):
    if x == "Clubs":
        return pd.Series([1., 0., 0., 0.])
    if x == "Diamonds":
        return pd.Series([0., 1., 0., 0.])
    if x == "Hearts":
        return pd.Series([0., 0., 1., 0.])
    return pd.Series([0., 0., 0., 1.])

def create_suites_data(data, cards_left, iters):
    suites = data.applymap(lambda x : x.suite)
    rounds = []
    y = []
    depth = len(data.columns) - cards_left - 1
    for i in range(iters):
        rounds.append(suites.loc[i,:depth].value_counts())
        y.append(suites.loc[i,depth + 1])
    data = pd.concat(rounds, axis=1).T
    data = data.reindex(sorted(data.columns), axis=1)

    scaler = MinMaxScaler()

    return pd.DataFrame(scaler.fit_transform(data), columns=data.columns).applymap(lambda x : 1 - x), pd.concat(list(map(edit_y_suites, y)), axis=1).T

# def create_suites_data(data, cards_left, iters):
#     suites = data.applymap(lambda x : x.suite)
#     rounds = []
#     y = []
#     depth = len(data.columns) - cards_left - 1
#     for i in range(iters):
#         rounds.append(suites.loc[i,:depth].value_counts())
#         y.append(suites.loc[i,depth + 1])
#     data = pd.concat(rounds, axis=1).T
#     data = data.reindex(sorted(data.columns), axis=1)

#     scaler = MinMaxScaler()

#     return pd.DataFrame(scaler.fit_transform(data), columns=data.columns).applymap(lambda x : 1 - x), pd.concat(list(map(edit_y_suites, y)), axis=1).T

def create_model(X_train, y_train, epochs):
    model = Sequential()
    model.add(Dense(10, input_dim=4, activation="relu"))
    model.add(Dense(10, activation="sigmoid"))
    model.add(Dense(4, activation="sigmoid"))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=epochs, batch_size=100)
    return model


if __name__ == "__main__":
    decks = 6
    iters = 10000
    cards_left = 52
    data = create_decks(decks, iters)
    X_train, y_train = create_suites_data(data, cards_left, iters)
    model = create_model(X_train, y_train, 200)
    model.save("cards/models/suite_prediction_model_1")
        
