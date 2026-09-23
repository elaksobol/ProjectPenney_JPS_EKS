# Based on our class example?

import numpy as np
from pathlib import Path
PATH_DECKS = Path('data/decks/')
PATH_SEED_LOG = Path('data/seed.json')
SEED_BASE = 1

def gen_decks(seed: int, 
               n_decks: int,
              ) -> np.ndarray:
    
    rng = np.random.default_rng(seed)

    deck = np.array([1]*26 + [0]*26)
    decks = np.empty((n_decks, 52), dtype = int)

    for i in range(n_decks):
        decks[i] = rng.permutation(deck)
        
    #return rng.integers(size=(n_decks))
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
    '''
    This doesn't actually save anything,
    it is just a demo of how I might construct
    the filename.
    '''
    PATH_DECKS.mkdir(parents=True, exist_ok=True)

    n_decks = decks.shape[0]

    packed = np.packbits(decks, axis = 1)

    filename = PATH_DECKS / f'decks_{n_decks}_seed_{seed}.bin'

    packed.tofile(filename)

    np.savez_compressed('...data/filename.npz', my_bits = packed)
    
    print(f'I might save this file like: {filename}')
    return filename









    