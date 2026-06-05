"""
Тема 14. Магические методы
"""


# Задание 1
# Создайте класс City с атрибутами name и population.
# Добавьте метод __str__(), который возвращает:
# Город <name>, население: <population>
# Создайте город и выведите его через print().


# TODO: решение
print(" ")
print("№1")
class City:
    def __init__(self, name, population):
        self.name = name
        self.population = population
    def __str__(self):
        return f"Город: {self.name}, население: {self.population}"


city = City("Москва", "12 миллионов человек")
print(city)

# Задание 2
# Создайте класс Movie с атрибутами title и year.
# Добавьте метод __repr__(), который возвращает строку:
# Movie(title='<title>', year=<year>)
# Проверьте вывод объекта.


# TODO: решение
print(" ")
print("№2")
class Movie:
    def __init__(self, title, year):
        self.title = title
        self.year = year

    def __repr__(self):
        return f"Movie(title={self.title!r}, year={self.year!r})"


movie = Movie("Book", 2009)
print(movie)

# Задание 3
# Создайте класс Point с атрибутами x и y.
# Добавьте метод __eq__(), чтобы две точки считались равными,
# если у них одинаковые x и y.
# Проверьте сравнение двух объектов через ==.


# TODO: решение
print(" ")
print("№3")
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


point1 = Point(5, 500)
point2 = Point(5, 500)

print(point1 == point2)

# Задание 4
# Создайте класс Playlist.
# Внутри храните список songs.
# Добавьте метод add_song(song).
# Добавьте метод __len__(), чтобы len(playlist) возвращал количество песен.


# TODO: решение
print(" ")
print("№4")
class Playlist:
    def __init__(self):
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def __len__(self):
        return len(self.songs)


play_list = Playlist()
play_list.add_song("Купить хлеб")
play_list.add_song("Сделать домашку")

print(len(play_list))


# Задание 5
# Создайте класс Package с атрибутами code и weight.
# Добавьте метод __lt__(), чтобы посылки сравнивались по весу.
# Проверьте выражение package1 < package2.


# TODO: решение
print(" ")
print("№5")
class Package:
    def __init__(self, code, weight):
        self.code = code
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight


package1 = Package("Book", 500)
package2 = Package("Phone", 30000)

print(package1 < package2)


# Задание 6
# Создайте класс Wallet с атрибутами owner и amount.
# Добавьте __str__(), который возвращает:
# Кошелек <owner>: <amount> руб.
# Добавьте __eq__(), который сравнивает кошельки по owner и amount.


# TODO: решение
print(" ")
print("№6")
class Wallet:
    def __init__(self, owner, amount):
        self.owner = owner
        self.amount = amount

    def __str__(self):
        return f"Кошелёк: {self.owner},  {self.amount} руб."
    
    def __eq__(self, other):
        return self.owner == other.owner and self.amount == other.amount
    
wallet1 = Wallet("Book", 500)
wallet2 = Wallet("Phone", 30000)
print(wallet1, wallet2)
print(wallet1 == wallet2)