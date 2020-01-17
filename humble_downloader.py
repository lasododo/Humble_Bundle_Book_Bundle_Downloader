import os
import time

from selenium import webdriver


MAXIMUM = 20
MAXIMUM2 = 20
XPATH_LINK = "/html/body/div[1]/div[3]/div[2]/div[{}]/div/div[2]/div[{}]/div[2]/div/div/span[2]"
TIMER = 1  # how long should you wait until script will continue ( depends on internet speed )


class BookCase:
    books = []

    def get_books(self):
        return self.books

    def add_book(self, book):
        self.books.append(book)

    def reload_books(self):
        for book in self.books:
            if book.downloaded:
                self.books.remove(book)


class Book:
    bookString = ""
    downloaded = False

    def __init__(self, book):
        self.bookString = book

    def get_book(self):
        return self.bookString

    def get_if_downloaded(self):
        return self.downloaded

    def set_downloaded(self, downloaded):
        self.downloaded = downloaded


def scrap_the_website(browser):
    book_case = BookCase()
    for div in range(3, MAXIMUM):
        for book in range(1, MAXIMUM2):
            try:
                book_text = browser.find_element_by_xpath(str(XPATH_LINK.format(div, book))).text
                book_case.add_book(Book(book_text))
                print(book_text)
            except Exception:
                break
    return book_case


def download_book_from_lib_genesis(browser, book):
    try:
        browser.get("http://gen.lib.rus.ec/")
        time.sleep(TIMER / 2)
        browser.find_element_by_xpath('//*[@id="searchform"]').send_keys(book.bookString)
        time.sleep(0.1)
        browser.find_element_by_xpath("/html/body/table/tbody[2]/tr/td[2]/form/input[2]").click()  # SUBMIT BUTTON
        time.sleep(TIMER)
        browser.find_element_by_xpath("/html/body/table[3]/tbody/tr[2]/td[3]/a").click()  # takes first link
        time.sleep(TIMER)
        browser.find_element_by_xpath("/html/body/table/tbody/tr[18]/td[2]/table/tbody/tr/td[1]/a").click()
        time.sleep(TIMER)
        browser.find_element_by_xpath("/html/body/table/tbody/tr/td[2]/h2/a").click()  # click GET
        time.sleep(TIMER)
        return True
    except AttributeError:
        raise AttributeError
    except Exception:
        return False


def book_downloader():
    pass


if __name__ == "__main__":
    link = input("link to HB bundle: ")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chromedriver = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver')
    chrome = webdriver.Chrome(chromedriver, chrome_options=chrome_options)
    chrome.get(link)
    time.sleep(TIMER)
    bookshelf = scrap_the_website(chrome)
    for book in bookshelf.books:
        book.set_downloaded(download_book_from_lib_genesis(chrome, book))
