from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as Chrome_options
import os, re, itertools


class WordChain:

    def __init__(self):

        self.URL = 'https://en.dict.naver.com/#/search?range=all&query='
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        self.DRIVER = 'chromedriver.exe'
        self.CHROME_OPTIONS = Chrome_options()
        self.CHROME_OPTIONS.add_argument("--incognito")
        self.CHROME_OPTIONS.add_argument("--headless")
        self.CHROME_OPTIONS.add_argument(f"user-agent={self.USER_AGENT}")
        self.driver = webdriver.Chrome(self.DRIVER, options=self.CHROME_OPTIONS)

    def search(self, word):
        self.driver.get(self.URL + word)

        meaning_list = []

        for i in range(10):
            try :
                meaning_list += WebDriverWait(self.driver, 2).until(
                    EC.presence_of_all_elements_located((By.XPATH, f'//*[@id="searchPage_entry"]/div/div[{i+1}]/ul')))
            except TimeoutException:
                break

        regex = re.compile(r"^.*([^.])$")
        meaning_list = [str(item.text).strip().split('\n') for item in meaning_list]
        meaning_list = list(itertools.chain.from_iterable([list(filter(regex.search, sublist)) for sublist in meaning_list]))
        meaning = ' // '.join(meaning_list).replace('((', '').replace('))', '')


        try:
            related_list = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_all_elements_located((By.XPATH, f'//*[@id="relationSearchArea"]/div')))
            related_list = [i for i in [str(item.text).strip().split(' ') for item in related_list][0] if i != '연관검색어']
        except Exception as e:
            print(e)
            related_list = []

        return meaning, related_list


if __name__ == "__main__":
    os.chdir(os.pardir)

    words = WordChain()
    meaning, related = words.search('will')
    print(meaning)
    print(related)

    for word in related:
        meaning, _ = words.search(word)
        print(word, meaning)

