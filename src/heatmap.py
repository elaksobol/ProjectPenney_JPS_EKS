
# Import statements
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# LABELS = the 8 possible sequences
# PATH_SCORES = where scores.csv is
from src.dataproc import LABELS, PATH_SCORES

# This is where the finished heatmaps go
PATH_FIGURES = Path('figures/')

# For heatmap purposes, we converted the 0s to Bs and the 1s to Rs
BR_LABELS = [label.replace('0', 'B').replace('1', 'R') for label in LABELS]


def load_totals():
  '''
  This function reads the CSV file of the game scores. It sums the counts of wins/ties and indexes
  them by player 1 or player 2. It outputs a pandas dataframe with all of the numeric values needed
  (cards_wins, cards_ties, tricks_wins, tricks_ties, and n_decks) summed.
  '''
  df = pd.read_csv(PATH_SCORES/'scores.csv', dtype={'P1': str,'P2': str})
  totals = df.groupby(['P1', 'P2']).sum(numeric_only=True)
  n_decks = totals['n_decks'].iloc[0]
  return totals, n_decks


def make_matrices(totals, n_decks, metric):
  '''
  This function turns the sums into two matrices and calculates the percentages of wins and ties.
  One matrix is for wins, one is for ties. It runs a nested for loop so all player sequence matchups
  are compared against each other (except for when P1 == P2, because that can't happen)
  '''
  wins = np.full((len(LABELS), len(LABELS)), np.nan)
  ties = np.full((len(LABELS), len(LABELS)), np.nan)

  for a, P1 in enumerate(LABELS):
    for b, P2 in enumerate(LABELS):
      if P1 == P2:
        continue
      wins[a, b] = totals.loc[(P1, P2), f'{metric}_wins'] / n_decks*100
      ties[a, b] = totals.loc[(P1, P2), f'{metric}_ties'] / n_decks*100
  return wins, ties



def plot_heatmap(wins, ties, n_decks, metric):
  '''
  This function contains all of the heatmap plotting code. The heatmaps were designed after the
  example designs shared on Blackboard, so diagonal cells are left blank (to ignore matching sequences).
  The heatmaps get saved to PATH_FIGURES.
  '''
  annot = []
  for b in range(len(LABELS)):
      row = []
      for a in range(len(LABELS)):
          if a == b:
              row.append('')
          else: 
              row.append(f'{wins[b, a]:.0f}({ties[b, a]:.0f})')
      annot.append(row)

  fig, ax = plt.subplots(figsize=(8,8))
  ax.set_facecolor('lightgray')

  sns.heatmap(wins, annot=annot, fmt='', cmap='Blues', cbar=False, square=True,
              linewidths=1, linecolor='white', vmin=0, vmax=100, xticklabels=BR_LABELS,
              yticklabels=BR_LABELS, ax=ax)
    
  ax.set_title(f'Probability of Win(Tie)\nScoring By {metric.capitalize()}\nN={n_decks:,}')
  ax.set_xlabel("Player Two")
  ax.set_ylabel("Player One")
  plt.yticks(rotation=0)

  PATH_FIGURES.mkdir(parents=True, exist_ok=True)
  filename = PATH_FIGURES / f'heatmap_{metric}.png'
  fig.savefig(filename, dpi=200, bbox_inches='tight')
  plt.close(fig)

  print(f'This file was saved as: {filename}')


def make_heatmaps():
  '''
  This function runs the whole process and is called by main.py. It loads the data,
  then makes and saves the two heatmaps (one for scoring by cards and one for scoring by tricks).
  '''
  totals, n_decks = load_totals()

  for metric in ('cards', 'tricks'):
    wins, ties = make_matrices(totals, n_decks, metric)
    plot_heatmap(wins, ties, n_decks, metric)





if __name__ == '__main__':
  make_heatmaps()
