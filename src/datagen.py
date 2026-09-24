
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
   
    PATH_DECKS.mkdir(parents=True, exist_ok=True)

    n_decks = decks.shape[0]

    packed = np.packbits(decks, axis = 1)

    filename = PATH_DECKS / f'decks_{n_decks}_seed_{seed}.npz'

    np.savez(filename, my_bits=packed, seed=seed)
    
    print(f'This file was saved as: {filename}')
    return filename









    