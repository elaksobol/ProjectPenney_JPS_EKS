

import numpy as np
from pathlib import Path

PATH_DECKS = Path('data/decks/')
PATH_SCORES = Path('data/scores/')

# red = 1, black = 0

LABELS = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']


def load_decks(filename: Path) -> ?:
    
    loaded_data = np.load(filename)
    
    decks = np.unpackbits(loaded_data['my_bits'], axis=1, count=52)
    # [:decks.size].reshape(decks.shape)
    # do we need this?
    
    seed = int(data['seed'])
    
    return decks, seed



def play_game() -> :
        tricks1 = 0
    tricks2 = 0
    cards1 = 0
    cards2 = 0





def score_decks(decks) -> dict:

    





def save_scores(scores:dict, seed:int) -> Path:
    
    PATH_SCORES.mkdir(parents=True, exist_ok=True)

    # n_decks = scores['?'].shape[2]
    
    filename = PATH_SCORES / f'scores_{n_decks}_seed_{seed}.npz'

   # np.savez_compressed(filename, seed=seed, **scores)

    print(f'This file was saved as: {filename}')
    return filename
    