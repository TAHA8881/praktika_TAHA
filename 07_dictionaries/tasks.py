"""
Тема 7. Словари
"""


# Задание 1
# Создайте словарь student с ключами:
# name, age, group.
# Выведите каждое значение отдельно.


# TODO: решение
print(" ")
print("№1")
student = {
    "name": "Anna",
    "age": 18,
    "group": "A1"
}
print(student)

# Задание 2
# Создайте словарь product с ключами title, price, count.
# Посчитайте общую стоимость товара: price * count.


# TODO: решение
print(" ")
print("№2")
product = {
    "title": "Anna",
    "price": 18,
    "count": 5
}
print('вывожу общую стоимость: ', product['price']*product['count'])

# Задание 3
# Дан словарь user = {"name": "Ivan", "email": "ivan@example.com"}.
# Добавьте ключ age со значением 20.
# Измените email на другой.
# Выведите итоговый словарь.


# TODO: решение
print(" ")
print("№3")
user = {"name": "Ivan", "email": "ivan@example.com"}
user["age"] = 19
user["email"] = "vania@example.com"
print(user)

# Задание 4
# Дан словарь scores = {"Anna": 5, "Ivan": 4, "Maria": 5, "Petr": 3}.
# Выведите имена студентов, у которых оценка 5.
print(" ")
print("№4")
scores = {"Anna": 5, "Ivan": 4, "Maria": 5, "Petr": 3}
if scores.get('Anna')==5:
    print('Anna')
if scores.get('Maria')==5:
    print('Maria')
if scores.get('Petr')==5:
    print('Petr')

# TODO: решение


# Задание 5
# Спросите у пользователя название страны.
# Есть словарь capitals:
# Russia -> Moscow
# France -> Paris
# Germany -> Berlin
# Если страна есть в словаре, выведите столицу.
# Если нет, выведите "Страна не найдена".
print(" ")
print("№5")
capitals = {
    "Russia": "Moscow",
    "France": "Paris",
    "Germany": "Berlin",
}

sity = input("Страна: ")
if sity in capitals:
#    for key, value in capitals.items():
        print(capitals[sity])
#else:
#    print("Страна не найдена")

# TODO: решение


# Задание 6
# Дан текст text = "apple banana apple orange banana apple".
# Посчитайте, сколько раз встречается каждое слово.
# Результат должен быть словарем.


# TODO: решение
print(" ")
print("№6")
text = "apple banana apple orange banana apple"
word=text.split()
words = {}

for word in words:
    if word in words:
        words[word] +=1
    else:
        words[word] = 1
print(words)