from db.db import VocabDB
from scrape.scraper import WordChain
from tqdm import tqdm
import os


def populate_db(seed, search_related=True):
    words = WordChain()
    db = VocabDB()
    meaning, related = words.search(seed)
    db.insert(seed, meaning, ', '.join(related))

    if search_related:
        print('[+] Searching for related words')
        for word in tqdm(related):
            meaning_, related_ = words.search(word)
            db.insert(word, meaning_, ', '.join(related_))


if __name__ == "__main__":
    os.chdir(os.pardir)
    populate_db("ephemeral")