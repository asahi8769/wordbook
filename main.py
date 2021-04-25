from problem import VocabProblem
from scrape.scraper import WordChain
from db.db import VocabDB
from tqdm import tqdm


def problem(how_many=5):
    n = 0
    scoring = []
    while n < how_many:
        probs = VocabProblem()
        problem = probs.pull()
        problem_dict = probs.populate_problem(problem)
        probs.show(problem_dict)
        scoring.append(int(probs.solve(problem_dict)*100/how_many))
    print(scoring, sum(scoring))


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


if __name__ == '__main__':

    action = int(input("What do you want? 1. Quiz, 2. Search : "))

    if action == 1:
        problem(how_many=5)

    if action == 2:
        word = input("Which word? : ")
        populate_db(word, search_related=True)

