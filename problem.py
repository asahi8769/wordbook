from db.db import VocabDB
from random import randint
import numpy as np


class VocabProblem:
    def __init__(self):
        self.db = VocabDB()
        self.id_list = self.db.col_to_list('ID')
        self.sel = {}

    def pull(self):
        avg_point = np.mean(self.db.col_to_list('POINTS'))
        avg_repeat = np.mean(self.db.col_to_list('REPEATS'))
        less_point = self.db.select_id_where(point=avg_point)
        less_seen = self.db.select_id_where(repeat=avg_repeat)
        print(avg_point, avg_repeat)


if __name__=='__main__':
    VocabProblem().pull()