from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from src.dataproc import score_decks, save_scores, save_score_summary
from src.datagen import gen_decks, get_next_seed, save_decks
from src.heatmap import make_heatmaps, PATH_FIGURES


def show_heatmaps():
  found_any=False
  for metric in ('cards', 'tricks'):
    filename = PATH_FIGURES / f'heatmap_{metric}.png'

    if not filename.exists():
      continue
    found_any=True

    made = datetime.fromtimestamp(filename.stat().st_mtime)
    print(f'Showing {filename} (made {made:%Y-%m-%d %H:%M})')

    fig, ax = plt.subplots(figsize=(8,8))
    ax.imshow(mpimg.imread(filename))
    ax.axis('off')
    fig.canvas.manager.set_window_title(f'Heatmap: {metric}')

  if found_any:
    plt.show(block = False)
  else:
    print('No heatmaps yet. Choose option 2 to add some decks first.')



def add_and_rescore():
    answer = input('How many decks would you like to add?')
    
    if not answer.isdigit() or int(answer) == 0:
        print('Please enter a whole number bigger than 0.')
        return

    n_decks = int(answer)
    seed = get_next_seed()
    decks = gen_decks(seed, n_decks)
    save_decks(decks, seed)
    scores = score_decks(decks)
    save_scores(scores, seed)
    save_score_summary()
    
    make_heatmaps()
    print('Done! Choose option 1 to see the updated heatmaps.')


if __name__ == '__main__':
  while True:
    print()
    print('1) See the most recent heatmaps')
    print('2) Add more decks, score them, and update the heatmaps')
    print('3) Quit')
    choice = input('Choose 1, 2, or 3: ')

    if choice == '1':
      show_heatmaps()
    elif choice == '2':
      add_and_rescore()
    elif choice == '3':
        print('Bye! ;-)')
        break
    else:
      print('Please type 1, 2, or 3.')