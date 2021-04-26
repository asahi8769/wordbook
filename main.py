from problem import VocabProblem
from scrape.scraper import WordChain
from db.db import VocabDB
from tqdm import tqdm


def problem(how_many=5):
    n = 0
    scoring = []
    while n < how_many:
        print(f"\n\n Problem no. {n+1}\n")
        probs = VocabProblem()
        problem = probs.pull()
        problem_dict = probs.populate_problem(problem)
        probs.show(problem_dict)
        scoring.append(int(int(probs.solve(problem_dict))*100/how_many))
        n += 1
    print("[+] Score :", sum(scoring))


def populate_db(seed, search_related=True, max=20):
    words = WordChain()
    db = VocabDB()
    meaning, related = words.search(seed)
    db.insert(seed, meaning, ', '.join(related))
    print(f"\n{seed} means :\n{meaning}\n")

    if search_related:
        print('[+] Searching for related words')
        for word in tqdm(related[:max]):
            meaning_, related_ = words.search(word)
            db.insert(word, meaning_, ', '.join(related_))


if __name__ == '__main__':
    while True:

        action = int(input("\nWhat do you want? 1. Quiz, 2. Search  3. Setting: "))

        if action == 1:
            problem(how_many=5)

        if action == 2:
            word = input("Which word? : ")
            populate_db(word, search_related=True, max=5)

        if action == 3:
            action = int(input("\nWhat do you want? 1. Reset Points, 2. Delete Table: "))
            db = VocabDB()

            if action == 1:
                db.reset_tick()

            if action == 2:
                db.delete_()
