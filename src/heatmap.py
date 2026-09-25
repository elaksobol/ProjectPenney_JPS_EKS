import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path


from dataproc import LABELS, PATH_SCORES

PATH_FIGURES = Path('figures/')

BR_LABELS = [label.replace('0', 'B').replace('1', 'R') for label in LABELS]


def load_totals():
  df = pd.read_csv(PATH_SCORES/'scores.csv', dtype={'P1': str,'P2': str})
  totals = df.groupby(['P1', 'P2']).sum(numeric_only=True)
  n_decks = totals['n_decks'].iloc[0]
  return totals, n_decks


def make_matrices(totals, n_decks, metric):
  wins = np.full((len(LABELS), len(LABELS)), np.nan)
  ties = np.full((len(LABELS), len(LABELS)), np.nan)

  for a, P1 in enumerate(LABELS):
    for b, P2 in enumerate(LABELS):
      if P1 == P2:
        continue
      wins[b, a] = totals.loc[(P1, P2), f'{metric}_wins'] / n_decks*100
      ties[b, a] = totals.loc[(P1, P2), f'{metric}_ties'] / n_decks*100
  return wins, ties



def plot_heatmap(wins, ties, n_decks, metric):
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
    ax.set_xlabel("My Choice")
    ax.set_ylabel("Opponent Choice")
    plt.yticks(rotation=0)

    PATH_FIGURES.mkdir(parents=True, exist_ok=True)
    filename = PATH_FIGURES / f'heatmap_{metric}.png'
    fig.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close(fig)

    print(f'This file was saved as: {filename}')


def make_heatmaps():
  totals, n_decks = load_totals()

  for metric in ('cards', 'tricks'):
    wins, ties = make_matrices(totals, n_decks, metric)
    plot_heatmap(wins, ties, n_decks, metric)





if __name__ == '__main__':
  make_heatmaps()
