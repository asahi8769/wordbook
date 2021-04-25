from db.db import VocabDB
from random import choices, shuffle
import numpy as np


class VocabProblem:
    def __init__(self):
        self.db = VocabDB()
        self.answer_key = 0
        self.answer_num = 0

    def pull(self):
        id_list = self.db.col_to_list('ID')
        points = self.db.col_to_list('POINTS')
        repeats = self.db.col_to_list('REPEATS')
        seq = [points[n]*0.6 + repeats[n]*0.4 for n in range(len(id_list))]

        points = [1-(i/(np.sum(seq)+0.0001)) for i in seq]
        while True:
            others = choices(id_list, k=4,  weights=[points[n] for n in range(len(id_list))])
            answer = choices(id_list, k=1, weights=[points[n] for n in range(len(id_list))])
            if answer[0] not in others and len(set(others)) == 4:
                self.answer_key = answer[0]
                break

        problem = others + answer
        shuffle(problem)

        return problem

    def populate_problem(self, problem):
        problem_dict = {}

        for id_ in problem:
            word, meaning, _, _ = self.db.search(id_=id_)
            problem_dict[id_] = {"word": word, "meaning": meaning}
        return problem_dict

    def show(self, problem_dict):
        print(f"\nWhat does '{problem_dict[self.answer_key]['word']}' means?\n")
        for n, key in enumerate(problem_dict.keys()):
            if key == self.answer_key:
                self.answer_num = n+1
            print(f" {n+1}. {problem_dict[key]['meaning']}")

    def solve(self, problem_dict):
        answer = int(input("\nYour answer? :"))
        if answer == self.answer_num:
            self.db.update_tick(word=None, id_=self.answer_key, point=1, repeat=1)
            print("\nYou are right!\n")
            print(f"{problem_dict[self.answer_key]['word']} means: \n {problem_dict[self.answer_key]['meaning']}\n")
            for n, key in enumerate(problem_dict.keys()):
                print(f" {n + 1}. {problem_dict[key]['word']} : {problem_dict[key]['meaning']}")
            return True

        else:
            self.db.update_tick(word=None, id_=self.answer_key, point=-5, repeat=0)
            print(f"\nWrong! The right answer is {self.answer_num}\n")
            print(f"{problem_dict[self.answer_key]['word']} means: \n {problem_dict[self.answer_key]['meaning']}\n")
            for n, key in enumerate(problem_dict.keys()):
                print(f" {n + 1}. {problem_dict[key]['word']} : {problem_dict[key]['meaning']}")
            return False


if __name__=='__main__':
    probs = VocabProblem()
    problem = probs.pull()
    problem_dict = probs.populate_problem(problem)
    probs.show(problem_dict)
    probs.solve(problem_dict)




