from .deck import Deck
from .deck import PokerCard
from random import randint
from time import sleep

# first neural network with keras tutorial
import numpy as np
import tensorflow as tf
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

def edit_y_values(x):
    if x == "2":
        return pd.Series([1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])
    if x == "3":
        return pd.Series([0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])
    if x == "4":
        return pd.Series([0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])
    if x == "5":
        return pd.Series([0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0.])
    if x == "6":
        return pd.Series([0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0.])
    if x == "7":
        return pd.Series([0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0.])
    if x == "8":
        return pd.Series([0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0.])
    if x == "9":
        return pd.Series([0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0.])
    if x == "10":
        return pd.Series([0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0.])
    if x == "J":
        return pd.Series([0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0.])
    if x == "Q":
        return pd.Series([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0.])
    if x == "K":
        return pd.Series([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0.])
    return pd.Series([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.])

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

def create_value_data(data, cards_left, iters):
    values = data.applymap(lambda x : x.value)
    rounds = []
    y = []
    depth = len(data.columns) - cards_left - 1
    for i in range(iters):
        rounds.append(values.loc[i,:depth].value_counts() / 4)
        y.append(values.loc[i,depth + 1])
    data = pd.concat(rounds, axis=1).T
    data = data.reindex(sorted(data.columns), axis=1)

    print(data)

    scaler = MinMaxScaler()

    return pd.DataFrame(scaler.fit_transform(data), columns=data.columns).applymap(lambda x : 1 - x), pd.concat(list(map(edit_y_values, y)), axis=1).T

def create_model(X_train, y_train, epochs):
    opt = tf.keras.optimizers.Adam(learning_rate=0.1)

    model = Sequential()
    model.add(Dense(26, input_dim=13, activation="sigmoid"))
    model.add(Dense(26, activation="sigmoid"))
    model.add(Dense(13, activation="sigmoid"))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=epochs, batch_size=100)
    return model

def add_card(card, series):
    new = series[::]
    if card.num_val < 10:
        new[card.num_val - 1] += 1
    if card.value == "10":
        new[9] += 1
    if card.value == "J":
        new[10] += 1
    if card.value == "Q":
        new[11] += 1
    if card.value == "K":
        new[12] += 1
    if card.value == "A":
        new[0] += 1
    return new

if __name__ == "__main__":
    model = tf.keras.models.load_model("cards/models/val_prediction_model_1")
    deck = Deck(PokerCard, num_decks=2)
    indices = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    all_series = []
    series = [0] * 13
    cards = []
    card = deck.deal()
    series = add_card(card, series)
    all_series.append(series)
    while len(deck) > 1:
        card = deck.deal()
        cards.append(add_card(card, [0] * 13))
        series = add_card(card, series)
        all_series.append(series)
    card = deck.deal()
    cards.append(add_card(card, [0] * 13))
    test_x = pd.concat(list(map(lambda x : (pd.Series(x) - pd.Series(x).min()) / (pd.Series(x) - pd.Series(x).min()).max(), all_series)), axis=1).T.applymap(lambda x : 1 - x)
    test_y = pd.DataFrame(cards)
    print(model.evaluate(test_x.loc[99:,:], test_y.loc[99:,:]))



        
