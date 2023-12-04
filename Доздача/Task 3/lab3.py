# Бібілотека для роботи з регулярними виразами
import re
import random

# Список з рандомними словами
with open("D:\\IT STEP\\2CS\\1 semester\\Python\\Доздача\\Task 3\\lorem.txt") as file:
    random_words = file.read().split(", ")
    random_words_list = []
    for i in random_words:
        random_words_list.append(i)
list_len = len(random_words_list)
def get_random_word():
    word = str(random_words_list[(random.randint(0, 62))])
    return word
def get_random_length():
    length = random.randint(3, 10)
    return length
# cls._inst зберігає единий екземпляр класу
class Singleton():
    _inst = None
    def __new__(cls):
        if (cls._inst is None):
           cls._inst = super().__new__(cls)
           return cls._inst
        else:
            print("The registry of pages exists already!")
    
    def __init__(self):
        self.pages = {}
        self.ids = []
        self.current_id = 0
    
    def get_random_id(self):
        not_unique = True
        while not_unique:
            self.current_id = random.randint(1, 2000)
            if self.current_id not in self.ids:
                not_unique = False
                self.ids.append(self.current_id)
                return self.current_id

    def print_all_books(self):
        for book in self.pages:
            print(f"{book}:")
            for page in self.pages[book]:
                ind = list(self.pages[book]).index(page) + 1
                print(f"Page {ind} (id: {page}): {self.pages[book][page]}")

class Book():
    book_num = 0
    def __init__(self, title, year, author, format, price):
        self.pages_list = {}
        self.title = title
        self.year = year
        self.author = author
        self.format = format
        self.price = price
    
    def print_all_info(self):
        print(f"Title: \"{self.title}\"\nYear: {self.year}\nAuthor: {self.author}\nFormat: {self.format}\nPrice: {self.price}$\n")

    def print_book_pages(self):
        print(f"Book: {self.title}")
        for page in self.pages_list:
            ind = list(self.pages_list).index(page) + 1
            print(f"Page {ind} (id: {page}): {self.pages_list[page]}")

class Builder():
    def __init__(self, title, year, author, format, price):
        self.elem = Book(title, year, author, format, price)

    def add_page(self, page_title):
        pages.get_random_id()
        id = pages.current_id
        self.elem.pages_list[id] = [page_title]

    def add_content(self, content):
        page_num = len(self.elem.pages_list)
        if page_num != 0:
            id = pages.current_id
            if id not in self.elem.pages_list:
                self.elem.pages_list[id] = [content]
            else:
                self.elem.pages_list[id].append(content)
        else:
            raise Exception("You should add a page first!")

    def create_book(self):
        Book.book_num += 1
        key = "Book " + str(Book.book_num)
        pages.pages[key] = self.elem.pages_list
        return self.elem

class ScienceBookBuilder(Builder):
    def __init__(self, title, year, author, format, price):
        super().__init__(title, year, author, format, price)
        self.refs = []
        self.glossary = {}

    def add_refs(self, ref):
        self.refs.append(ref)
        self.elem.refs = self.refs
        self.add_content(ref)

    def add_words(self, word, meaning):
        if word not in self.glossary.keys():
            self.glossary[word] = meaning
            self.elem.glossary = self.glossary
            self.add_content(f"{word}: {meaning}")
            
class NovelBookBuilder(Builder):
    def __init__(self, title, year, author, format, price):
        super().__init__(title, year, author, format, price)
        self.characters_list = {}

    def add_chars(self, character, desc):
        if character not in self.characters_list.keys():
            self.characters_list[character] = desc
            self.elem.characters_list = self.characters_list
            self.add_content(f"{character}: {desc}")

class ManualBookBuilder(Builder):
    def __init__(self, title, year, author, format, price):
        super().__init__(title, year, author, format, price)
        self.links_list = []
    def add_link(self, link):
        if re.match("^(https:/\/\).+((.jpg)$|(.png)$|(.jpeg)))", link):
            self.links_list.append(link)
            self.elem.links_list = self.links_list
            self.add_content(link)
        else:
            raise Exception("Invalid link!")

class RandomBookBuilder(Builder):
    pages_amount = random.randint(1, 5)

    def create_sentence(self):
        words_amount = random.randint(3, 10)
        sentence = ""
        for i in range(words_amount):
            if i == 0:
                word = get_random_word().capitalize() + " "
            else:
                word = get_random_word() + " "
            sentence += word
        sentence = sentence.strip()
        sentence += "."
        return sentence

    def create_title(self):
        title = ""
        length = get_random_length()
        for _ in range(length):
            word = get_random_word().capitalize() + " "
            title += word
        return title.strip()
    
    def create_author(self):
        author = get_random_word().capitalize() + " " + get_random_word().capitalize()
        return author
    
    def __init__(self):
        title = RandomBookBuilder.create_title(self)
        author = RandomBookBuilder.create_author(self)
        year = random.randint(1990, 2023)
        format = "A" + str(random.randint(3, 6))
        price = random.randint(1, 100)
        super().__init__(title, year, author, format, price)

    def add_page(self):
        for _ in range(RandomBookBuilder.pages_amount):
            pages.get_random_id()
            id = pages.current_id
            sentence = RandomBookBuilder.create_sentence(self)
            page_title = RandomBookBuilder.create_sentence(self)
            self.elem.pages_list[id] = [page_title]
            self.elem.pages_list[id] = [sentence]        

pages = Singleton()

book1 = ScienceBookBuilder("Science", 1999, "Name", "A4", 10)
book1.add_page("Name1")
book1.add_refs("ref")
book1.add_refs("ref")
book1.add_content("content")
book1.add_page("Name3")
book1.add_refs("ref")
book1.add_page("Name4")
book1.add_page("Name5")
book1.add_words("word1", "meaning1")
book1.add_words("word2", "meaning2")
ready_book1 = book1.create_book()

random_book = RandomBookBuilder()
random_book.add_page()
random_book_ready = random_book.create_book()
random_book_ready.print_all_info()

book2 = ManualBookBuilder("Manual", 1999, "Name", "A4", 20)
book2.add_page("Name1")
book2.add_link("https://i.pinimg.com/564x/81/7f/ba/817fba5a0e96bc1076b105720fc3569c.jpg")
book2.add_link("https://i.pinimg.com/564x/69/ff/c4/69ffc42ba1c739e25ed76fcaa6555a0e.jpg")
book2.add_page("Name2")
ready_book2 = book2.create_book()

ready_book1.print_all_info()
ready_book2.print_all_info()

print("All books:")
pages.print_all_books()

random_book_ready.print_book_pages()


