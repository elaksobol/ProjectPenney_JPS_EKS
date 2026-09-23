import src.datagen as datagen

from pathlib import Path

my_path = Path("src") / 'datagen.py'

datagen.gen_decks(1, 5)