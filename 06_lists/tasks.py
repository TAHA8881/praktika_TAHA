"""
Тема 6. Списки
"""


# Задание 1
# Создайте список из пяти любимых продуктов.
# Выведите первый, третий и последний элемент.


# TODO: решение
print("№1")
prdukt = ["каша", "яблоко", "торт", "макаруны"]
print(prdukt[0])   # Anna
print(prdukt[2])   # Anna
print(prdukt[-1])  # Maria

# Задание 2
# Создайте список чисел [3, 7, 1, 9, 4].
# Выведите сумму, минимальное и максимальное число.


# TODO: решение
print(" ")
print("№2")

numbers=[3, 7, 1, 9, 4]
print(sum(numbers))
print(min(numbers))
print(max(numbers))



# Задание 3
# Создайте пустой список.
# Спросите у пользователя три имени и добавьте их в список.
# Выведите итоговый список.


# TODO: решение
print(" ")
print("№3")
pustoi=[]
a=input("Выведите имя: ")
b=input("Выведите имя: ")
c=input("Выведите имя: ")
pustoi.append(a)
pustoi.append(b)
pustoi.append(c)
print(pustoi)

# Задание 4
# Дан список numbers = [1, 2, 3, 4, 5, 6, 7, 8].
# Создайте новый список только из четных чисел.


# TODO: решение
print(" ")
print("№4")
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
print(numbers[1::2])

# Задание 5
# Дан список grades = [5, 4, 3, 5, 2, 4, 5].
# Посчитайте среднюю оценку.
print(" ")
print("№5")
grades = [5, 4, 3, 5, 2, 4, 5]


# TODO: решение

s=(sum(numbers))
l=(len(numbers))
print(s/l)

# Задание 6
# Спросите у пользователя пять чисел.
# Добавьте их в список.
# Выведите список в отсортированном виде.


# TODO: решение
print(" ")
print("№6")
chisla=[]
a =int(input("Выведите пять чисел: "))
b =int(input())
c =int(input())
d =int(input())
e =int(input())
chisla.append(a)
chisla.append(b)
chisla.append(c)
chisla.append(d)
chisla.append(e)
print(sorted(chisla))