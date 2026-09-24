

import csv


import numpy as np
from pathlib import Path

PATH_DECKS = Path('data/decks/')
PATH_SCORES = Path('data/scores/')

METRICS = ('tricks', 'cards')

# red = 1, black = 0

LABELS = ['000', '001', '010', '011', '100', '101', '110', '111']


def load_decks(filename: Path) -> ?:
    
    loaded_data = np.load(filename)    
    decks = np.unpackbits(loaded_data['my_bits'], axis=1, count=52)    
    seed = int(loaded_data['seed'])   
    return decks, seed


def deck_to_strings(decks) -> list[str]:
    chars = decks.astype(np.uint8) + ord('0')
    return [row.tobytes()decode() for row in chars]


def not_found_to_inf(idx: int) -> :
    return np.inf if idx == -1 else idx


def play_game(deck, P1, P2) -> :
    tricks1 = 0
    tricks2 = 0
    cards1 = 0
    cards2 = 0

    start = 0

    while True:
        idx1 = not_found_to_inf(deck.find(P1, start))
        idx2 = not_found_to_inf(deck.find(P2, start))

        idx = min(idx1, idx2)

        if idx == np.inf: # if neither sequence shows up, game over
            break

        end = int(idx)+3

        if idx1 < idx2:
            tricks1 += 1
            cards1 += end - start
        else:
            tricks2 += 1
            cards2 += end - start
        start = end

    return tricks1, tricks2, cards1, cards2

    
    

# one P1, one P2, who won/tied each scoring method
def score_game(deck, P1, P2) -> :
    tricks1, tricks2, cards1, cards2 = play_game(deck, P1, P2)

    return int(np.sign(tricks1 - tricks2)), int(np.sign(cards1 - cards2))





# for P1 in LABELS, for P2 in LABELS... run score game function
def score_games(deck) -> np.ndarray:
    # can we make this 2 x 8 x 8
    score_results = np.zeros((len(METRICS), len(LABELS), len(LABELS)), dtype=np.int8)

    for a, P1 in enumerate(LABELS):
        for b, P2 in enumerate(LABELS):
            if P1 == P2:
                continue
            score_results[:, a, b] = score_game(deck, P1, P2)

    return score_results

    
    

# for deck in decks, run scoregames function   
def score_decks(decks) -> dict:
    deck_strings = decks_to_strings(decks)
    deck_results = np.zeros((len(METRICS), len(LABELS), len(LABELS), len(deck_strings)), dtype=np.int8)

    






# for seed in seeds, run score_decks?
def score_seeds()







def save_scores(scores:dict, seed:int) -> Path:
    
    PATH_SCORES.mkdir(parents=True, exist_ok=True)

    # n_decks = scores['?'].shape[2]
    
    filename = PATH_SCORES / f'scores_{n_decks}_seed_{seed}.npz'

   # np.savez_compressed(filename, seed=seed, **scores)

    print(f'This file was saved as: {filename}')
    return filename







   # for P1 in LABELS:
    #    for P2 in LABELS:
            ## make sure string does not match