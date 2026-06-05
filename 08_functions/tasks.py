"""
Тема 8. Функции
"""


# Задание 1
# Напишите функцию greet(name), которая выводит:
# Привет, <name>!
# Вызовите функцию три раза с разными именами.


# TODO: решение
print(" ")
print("№1")
def greet(name):
    print(f"Hello", {name})

greet("Anna")
greet("Ivan")
greet("Vasia")


# Задание 2
# Напишите функцию add(a, b), которая возвращает сумму двух чисел.
# Вызовите функцию и выведите результат.


# TODO: решение
print(" ")
print("№2")
def add(a, b):
    return a + b

result = add(3, 5)
print(result)

# Задание 3
# Напишите функцию is_even(number), которая возвращает True,
# если число четное, и False, если нечетное.
# Проверьте функцию на нескольких числах.


# TODO: решение
print(" ")
print("№3")
def is_even(number):
    return number % 2 == 0

n=int(input('Введите число: '))
if is_even(n):
    print('True')
else:
    print('False')


# Задание 4
# Напишите функцию get_max(a, b, c), которая возвращает наибольшее
# из трех чисел.


# TODO: решение
print(" ")
print("№4")
m=0
def get_max(a, b, c):
    if a>b>c:
        m=a
    elif a<b<c:
        m=c
    else:
        m=b

    return m

a=int(input('Введите число: '))
b=int(input('Введите число: '))
c=int(input('Введите число: '))

print(get_max(a,b,c))


# Задание 5
# Напишите функцию count_vowels(text), которая считает количество
# гласных букв в строке.
# Можно считать гласными: a, e, i, o, u, y.


# TODO: решение
print(" ")
print("№5")
i = 0
a = 0
e = 0
i = 0
o = 0 
u = 0
y = 0
glassnie = 0
def count_vowels(input_text):
    a = input_text.lower().count('a')
    e = input_text.lower().count('e')
    i = input_text.lower().count('i')
    o = input_text.lower().count('e') 
    u = input_text.lower().count('u')
    y = input_text.lower().count('y')
    glassnie = a+e+i+o+u+y
    return glassnie

predlo=input("Выведите предложение: ")

print(count_vowels(predlo))


# Задание 6
# Напишите функцию calculate_total(price, count, discount=0).
# Функция должна возвращать итоговую стоимость:
# price * count минус скидка в процентах.
# Пример: price=100, count=3, discount=10 -> 270.


# TODO: решение
print(" ")
print("№6")
price=0
count=0
discount=0
total_price=0
def calculate_total(price, count, discount):
    total_price=price*count-discount
    return(total_price)
    
price=int(input('Введите цену: '))
count=int(input('Введите число товаров: '))
discount=int(input('Введите скидку: '))
print(calculate_total(price, count, discount))