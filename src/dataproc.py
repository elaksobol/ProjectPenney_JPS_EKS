

import csv


import numpy as np
from pathlib import Path

PATH_DECKS = Path('data/decks/')
PATH_SCORES = Path('data/scores/')

# the two scoring methods

METRICS = ('tricks', 'cards')

# red = 1, black = 0
#these are all the possible three card sequences

LABELS = ['000', '001', '010', '011', '100', '101', '110', '111']


def load_decks(filename: Path) -> tuple[np.ndarray, int]:
    '''
    This takes the bitpacked zipped file and unpacks each one. This returns the array of decks unpacked decks as 
    well as the seed that was used to create them. 
    '''
    
    loaded_data = np.load(filename)    
    decks = np.unpackbits(loaded_data['my_bits'], axis=1, count=52)    
    seed = int(loaded_data['seed'])   
    return decks, seed


def get_unscored_decks() -> list[Path]:
    '''
    This is used to make sure that the program does not rerun each deck if those decks were already 
    used within a game. Through looking at the .npz files, this function looks through each one to see if 
    they have a corresponding scored file that would look like scores_10_seed_1.npz. If there is no scored file 
    then the function appends all the unscored decks into the unscored_decks list.
    '''
    deck_files = list(PATH_DECKS.glob('*.npz'))

    unscored_decks = []

    for deck_file in deck_files:
        score_file = PATH_SCORES / f'scores_{deck_file.stem.removeprefix("decks_")}.npz'

        if not score_file.exists():
            unscored_decks.append(deck_file)

    return unscored_decks


def deck_to_strings(decks: np.ndarray) -> list[str]:
    '''
    This function changes the arrays into a list of strings. Through looking at every row in decks, converting the ints to 
    strings, and then joining them together in each row.
    '''
    return [''.join(map(str, row)) for row in decks]


def not_found_to_inf(idx: int) -> float:
    '''
    This function helps the play_game function. Since we have a list of if statements for the game, it is 
    important to have an instance in which neither card was found. That would create a -1 but to keep our current 
    statements, we changed a -1 value to infinity so it is not the minimum. This allows the game to continue on correctly. 
    '''
    if idx == -1:
        return np.inf
    else:
        return idx


def play_game(deck, P1, P2) -> tuple[int, int, int, int]:
    '''
    This function actually plays the game. However it starts small and only plays with one deck at a time. Starting each 
    player's trick and card score at 0, the game begins. Using the string find method, the game looks through the sequence
    to find the player's choices. After they are found, the locations of the first instance they were located is compared. 
    The smallest (meaning the first in the deck of cards) becomes the the index that is used. To locate the end of the 
    sequence, and become the new start point of deck the code adds three to their location. Then the scoring begins by 
    looking at the location of the found sequence. Depending on which sequence was found first, the appropriate scoring is 
    added. The loop ends when neither sequence shows up. 
    '''
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
    '''
    This scores a single game with a single deck. Looking at the scoring that was created through play_game, this function
    compares player one and player two's scores to see who won the game and if there was a tie. If player one has more tricks,
    the trick_results is positive, while inversely if player two wins the result is negative, with a tie being the middle of 0.
    '''
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
    '''
    This scores every possible sequence against each other for one deck. Through making a array of the scoring way, player
    one's possible sequence, player two's possible sequences (a 2x8x8), the for loop goes through each and records the score
    of each combination. 
    '''
    score_results = np.zeros((len(METRICS), len(LABELS), len(LABELS)), dtype=np.int8)

    for a, P1 in enumerate(LABELS):
        for b, P2 in enumerate(LABELS):
            if P1 == P2:
                continue
            score_results[:, a, b] = score_game(deck, P1, P2)

    return score_results

    
    

# for deck in decks, run scoregames function   
def score_decks(decks: np.ndarray) -> np.ndarray:
    '''
    This function grows upon score_games to now include multiple decks. This first calls to make the decks strings, and then 
    creates an item to stores the results in a 2x8x8xdecks array. Then a loop goes through every deck of cards in the unscored
    deck of strings. 
    '''
    deck_strings = deck_to_strings(decks)
    deck_results = np.zeros((len(METRICS), len(LABELS), len(LABELS), len(deck_strings)), dtype=np.int8)

    for i, deck in enumerate(deck_strings):
        deck_results[:, :, :, i] = score_games(deck)

    return deck_results




def save_scores(scores:np.ndarray, seed:int) -> Path:
    '''
    This function saves the result of each deck and each combination of card sequences for both scoring ways. It saves it 
    in a .npz file that represents the scored deck. 
    '''
    
    PATH_SCORES.mkdir(parents=True, exist_ok=True)

    n_decks = scores.shape[3]
    
    filename = PATH_SCORES / f'scores_{n_decks}_seed_{seed}.npz'
    
    np.savez_compressed(filename, seed = seed, scores = scores)

    print(f'This file was saved as: {filename}')
    
    return filename




    

def save_score_summary() -> Path:
    '''
    This function creates the .csv file of all the wins and ties for each probability coombination for the two scoring ways. 
    It loads each scored file into a list and combines them to write the .csv file which adds up each option of wins and ties.
    '''
    PATH_SCORES.mkdir(parents=True, exist_ok=True)
    filename = PATH_SCORES / 'scores.csv'
    score_files = list(PATH_SCORES.glob('scores_*.npz'))
    if not score_files:
        print('No score files found.')
        return filename

    score_list = []

    for score_file in score_files:
        loaded_data = np.load(score_file)
        score_list.append(loaded_data['scores'])

    all_scores = np.concatenate(score_list, axis = 3)
    n_decks = all_scores.shape[3]

    with filename.open('w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(['n_decks', 'P1', 'P2', 'tricks_wins', 'tricks_ties', 'cards_wins', 'cards_ties'])

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
    '''
    This runs the code so when the uses runs main.py every function will run. 
    '''
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
