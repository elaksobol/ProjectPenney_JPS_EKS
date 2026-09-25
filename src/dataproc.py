

import csv


import numpy as np
from pathlib import Path

PATH_DECKS = Path('data/decks/')
PATH_SCORES = Path('data/scores/')

METRICS = ('tricks', 'cards')

# red = 1, black = 0

LABELS = ['000', '001', '010', '011', '100', '101', '110', '111']


def load_decks(filename: Path) -> tuple[np.ndarray, int]:
    
    loaded_data = np.load(filename)    
    decks = np.unpackbits(loaded_data['my_bits'], axis=1, count=52)    
    seed = int(loaded_data['seed'])   
    return decks, seed


def get_unscored_decks() -> list[Path]:
    deck_files = list(PATH_DECKS.glob('*.npz'))

    unscored_decks = []

    for deck_file in deck_files:
        score_file = PATH_SCORES / f'scores_{deck_file.stem.removeprefix("decks_")}.npz'

        if not score_file.exists():
            unscored_decks.append(deck_file)

    return unscored_decks



def deck_to_strings(decks: np.ndarray) -> list[str]:
    chars = decks.astype(np.uint8) + ord('0')
    return [row.tobytes().decode() for row in chars]


def not_found_to_inf(idx: int) -> float:
    if idx == -1:
        return np.inf
    else:
        return idx


def play_game(deck, P1, P2) -> tuple[int, int, int, int]:
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
def score_game(deck, P1, P2) -> tuple[int, int]:
    tricks1, tricks2, cards1, cards2 = play_game(deck, P1, P2)

    if tricks1 > tricks2:
        trick_result = 1
    elif tricks1 < tricks2:
        trick_result = -1
    else:
        trick_result = 0

    if cards1 > cards2:
        card_result = 1
    elif cards1 < cards2:
        card_result = -1
    else:
        card_result = 0

    return trick_result, card_result





# for P1 in LABELS, for P2 in LABELS... run score game function
def score_games(deck: str) -> np.ndarray:
    # can we make this 2 x 8 x 8
    score_results = np.zeros((len(METRICS), len(LABELS), len(LABELS)), dtype=np.int8)

    for a, P1 in enumerate(LABELS):
        for b, P2 in enumerate(LABELS):
            if P1 == P2:
                continue
            score_results[:, a, b] = score_game(deck, P1, P2)

    return score_results

    
    

# for deck in decks, run scoregames function   
def score_decks(decks: np.ndarray) -> np.ndarray:
    deck_strings = deck_to_strings(decks)
    deck_results = np.zeros((len(METRICS), len(LABELS), len(LABELS), len(deck_strings)), dtype=np.int8)

    for i, deck in enumerate(deck_strings):
        deck_results[:, :, :, i] = score_games(deck)

    return deck_results




def save_scores(scores:np.ndarray, seed:int) -> Path:
    
    PATH_SCORES.mkdir(parents=True, exist_ok=True)

    n_decks = scores.shape[3]
    
    filename = PATH_SCORES / f'scores_{n_decks}_seed_{seed}.npz'
    
    np.savez_compressed(filename, seed = seed, scores = scores)

    print(f'This file was saved as: {filename}')
    
    return filename




    


def save_score_summary() -> Path:
    PATH_SCORES.mkdir(parents=True, exist_ok=True)
    filename = PATH_SCORES / 'scores.csv'
    score_files = list(PATH_SCORES.glob('scores_*.npz'))
    if not score_files:
        print('No score files found.')
        return filename

    score_list = []

    for score_file in score_files:
        loaded_data = np.load(score_file)
        scores_list.append(loaded_data['scores'])

    all_scores = np.concatenate(scores_list, axis = 3)
    n_decks = all_scores.shape[3]

    with filename.open('w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(['n_decks', 'P1', 'P2', 'trick wins', 'trick ties', 'card wins', 'card ties'])

        for a, P1 in enumerate(LABELS):
            for b, P2 in enumerate(LABELS):
                if P1 == P2:
                    continue

                trick_wins = np.sum(all_scores[0, a, b, :] == 1)
                trick_ties = np.sum(all_scores[0, a, b, :] == 0)
                card_wins = np.sum(all_scores[1, a, b, :] == 1)
                card_ties = np.sum(all_scores[1, a, b, :] == 0)

                writer.writerow([n_decks, P1, P2, trick_wins, trick_ties, card_wins, card_ties])

    print(f'This file was saved as: {filename}')
    return filename


if __name__ == '__main__':
    unscored_decks = get_unscored_decks()

    for filename in unscored_decks:
        decks, seed = load_decks(filename)
        scores = score_decks(decks)
        save_scores(scores, seed)

    save_score_summary()




    








   # for P1 in LABELS:
    #    for P2 in LABELS:
            ## make sure string does not match
    ## for seed in seeds, run score_decks?
        #def score_seeds()