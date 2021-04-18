import sqlite3


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










