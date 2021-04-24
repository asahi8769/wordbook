import sqlite3
from tqdm import tqdm
from scrape.scraper import WordChain


class VocabDB:
    def __init__(self):
        self.db_name = 'db/VocabDB.db'
        self.create()

    def create(self):
        try :
            with sqlite3.connect(self.db_name) as conn:
                cur = conn.cursor()
                cur.execute(
                    ''' CREATE TABLE "ENG" (
                                `ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                                `WORD` TEXT NOT NULL UNIQUE, 
                                `MEANING` TEXT, 
                                `RELATED_WORDS` TEXT, 
                                `POINTS` INTEGER NOT NULL DEFAULT 0, 
                                `REPEATS` INTEGER NOT NULL DEFAULT 0 )   '''
                )
                conn.commit()

                cur.execute(
                    ''' CREATE UNIQUE INDEX `INDEX` ON `ENG` ( `ID` ASC, `WORD` )   '''
                )
                conn.commit()
        except sqlite3.OperationalError:
            print(f'[-] DB already exists [{self.db_name}]')

    def length(self):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            query = ''' SELECT COUNT(*) FROM ENG '''
            cur.execute(query)
            return cur.fetchone()[0]

    def insert(self, *args):
        try :
            with sqlite3.connect(self.db_name) as conn:
                cur = conn.cursor()
                cur.execute(
                    ''' INSERT INTO ENG(WORD, MEANING, RELATED_WORDS)
                                  VALUES(?,?,?) ''',
                    args
                )
                conn.commit()
        except sqlite3.IntegrityError:
            print(f"[-] Unique constraint violated [{args[0]}]")
            pass

    def drop(self, word):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                ''' DELETE from ENG where WORD = ? ''',
                (word,)
            )
            conn.commit()

    def last_id(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cur = conn.cursor()
                query = ''' SELECT ID FROM ENG '''
                cur.execute(query)
                return cur.fetchall()[-1][0]
        except IndexError:
            return 0

    def index_list(self):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            query = ''' SELECT ID FROM ENG '''
            cur.execute(query)
            return [i[0] for i in cur.fetchall()]

    def search(self, word=None, id_=None):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            query = ''' SELECT WORD, MEANING, POINTS, REPEATS FROM ENG WHERE WORD=? OR ID=? '''
            cur.execute(query, (word, id_,))
            conn.commit()
            reference = cur.fetchone()

        word = reference[0]
        meaning = reference[1]
        point = reference[2]
        repeat = reference[3]
        return word, meaning, point, repeat

    def select_id_where(self, pt=1):
        with sqlite3.connect (self.db_name) as conn:
            cur = conn.cursor ()
            query = ''' SELECT ID FROM ENG
                        WHERE POINTS < ? OR REPEATS < ?'''
            cur.execute (query, (pt, pt,))
            return [i[0] for i in cur.fetchall()]

    def update_tick_right(self, word=None, id=None, point=0, repeat=0):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            query = ''' UPDATE ENG 
                        SET POINTS = POINTS +?,
                            REPEATS = REPEATS +?
                        WHERE WORD=? OR ID=? '''
            cur.execute(query, (point, repeat, word, id))
            conn.commit()


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
    import os

    os.chdir(os.pardir)
    db = VocabDB()
    db.create()

    length = db.length()
    print(length)

    # db.insert('word_', '단어', 'saying')
    #
    # db.drop('word')
    num = db.last_id()
    print(num)

    id_list = db.index_list()
    print(id_list)

    a = db.search(id_=3, word=None)
    print(a)

    ls = db.select_id_where(pt=1)
    print(ls)

    db.update_tick_right(word='erratic',id=None, point=1, repeat=0)









