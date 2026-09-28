
import numpy as np
from pathlib import Path
import json
from datetime import datetime as dt



PATH_DECKS = Path('data/decks/')
PATH_SEED_LOG = Path('data/seed.json')
SEED_BASE = 1

def gen_decks(seed: int, 
               n_decks: int,
              ) -> np.ndarray:
    '''
    Generate the decks according to what the user inputs for n_decks. It uses a random number generation object according to the seed, which is incremented by one in the get_next_seed function. Each deck is an array of equal 1s (reds) and 0s (blacks). We then created an empty array to hold all the decks after they are shuffled. For each we choose to use uint8 as we found it uses less memory. We then looped through each array of 52 cars and shuffle them.
    '''
    
    rng = np.random.default_rng(seed)

    # dtype = np.uint8 uses 8x less memory before packing, nothing else changes
    deck = np.array([1]*26 + [0]*26, dtype=np.uint8)
    decks = np.empty((n_decks, 52), dtype=np.uint8)

    for i in range(n_decks):
        decks[i] = rng.permutation(deck)
        
    return decks




def get_next_seed() -> int:
    '''
    Read the last seed used, increment by 1,
    and update seed.json.

    This was sourced from our class code notes.
    '''
    # Make sure the parent directory(s) exists
    PATH_SEED_LOG.parent.mkdir(parents=True, exist_ok=True)

    # Determine the next seed
    if not PATH_SEED_LOG.exists():
        print(f'No seed log found, starting with {SEED_BASE}')
        seed = SEED_BASE
    else:
        with PATH_SEED_LOG.open('r') as f:
            seed_log = json.load(f)
        seed = seed_log['seed'] + 1

    # Update the log
    seed_log = {
        'seed': seed,
        'seed_time': str(dt.now())
    }
    with PATH_SEED_LOG.open('w') as f:
        json.dump(seed_log, f)
    
    return seed




def save_decks(decks: np.ndarray, 
               seed: int
              ) -> Path:
    '''
    This function takes in the incremented seed and the now filled array of the shuffled decks and after checking the paths, we bitpacked. We saved each bitpacked array using the number for n_decks and the seed for easy understanding. After we saved each bitpacked file as a numpy zipped file. 
    '''
   
    PATH_DECKS.mkdir(parents=True, exist_ok=True)

    n_decks = decks.shape[0]

    packed = np.packbits(decks, axis = 1)

    filename = PATH_DECKS / f'decks_{n_decks}_seed_{seed}.npz'

    np.savez(filename, my_bits=packed, seed=seed)
    
    print(f'This file was saved as: {filename}')
    return filename









    