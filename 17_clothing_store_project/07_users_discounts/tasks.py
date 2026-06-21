"""
Этап 07. Пользователи и скидки

Цель: добавить адреса доставки, промокоды и отдельную логику расчета скидок.

Модели адреса и промокода, их репозитории и сервис скидок создавайте прямо в этом файле.
Покупателя и сервис заказов импортируйте из предыдущих этапов.
"""


# Задание 1 :)
# Расширьте модель покупателя.
# Добавьте данные, которые нужны для связи и доставки.


# TODO: расширить данные покупателя
class Delivery:
    def __init__(self, byer_id, byer_name, byer_email, byer_telephone, address, promcode):
        if byer_id <= 0:
            raise ValueError("Идентификатор покупателя  должен быть положительным")

        if byer_name == "":
            raise ValueError("Имя покупателя не может быть пустым")

        if "@" not in byer_email:
            raise ValueError("Некорректный email")

        if  byer_telephone == "":
            raise ValueError("Телефон покупателя не может быть пустым")
        
        if address == "":
            raise ValueError("Координаты покупателя не может быть пустыми")
        
        if promcode == "":
            raise ValueError("Промокод покупателя не может быть пустым")

        self.byer_id = byer_id
        self.byer_name = byer_name
        self.byer_email = byer_email
        self.byer_telephone = byer_telephone
        self.address = address
        self.promcode = promcode

    def __str__(self):
        return(f'{self.byer_id}, {self.byer_name}, {self.byer_email}, {self.byer_telephone}, {self.address}, {self.promcode}')
   
    def __repr__(self):
        return(f'{self.byer_id}, {self.byer_name}, {self.byer_email}, {self.byer_telephone}, {self.address}, {self.promcode}')

# Задание 2
# Расширьте SQL-схему таблицами адресов доставки и промокодов.
# Продумайте внешние ключи, уникальность кода промокода и обязательные поля.


# TODO: добавить таблицы адресов и промокодов в schema.sql


# Задание 3  ✔
# Опишите адрес доставки отдельной моделью.
# Продумайте обязательные поля и простые проверки.


# TODO: добавить модель адреса


# Задание 4
# Создайте репозиторий адресов доставки.
# Покупатель может иметь один или несколько адресов.


# TODO: добавить репозиторий адресов доставки
class AddressRepository:

    def __init__(self, connection):
        self.connection= connection 

    def add_address(self, address):
        query = """
            INSERT INTO delivery (byer_id, byer_name, byer_email, byer_telephone, address)
            VALUES (%s, %s, %s, %s, %s)
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (address.byer_id, address.byer_name, address.byer_email, address.byer_telephone, address.address, address.promcode))

        self.connection.commit()

    def get_adress_by_byer_id(self, byer_id):
        query = """
            SELECT address
            FROM delivery
            WHERE byer_id = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (byer_id,))
            rows = cursor.fetchall()
            addresses = []
        for row in rows:
            addresses.append(Delivery(byer_id, row [0], row [1], row [3] ))

        return addresses
 

# Задание 5
# Опишите промокод.
# Продумайте код, размер скидки, активность и минимальную сумму.


# TODO: добавить модель промокода
class PromoCode:
    def __init__(self, code, percent, min_total, is_active=True):
        self.code = code
        self.percent = percent
        self.min_total = min_total
        self.is_active = is_active

# Задание 6
# Создайте репозиторий промокодов.
# Поиск промокода должен быть удобным для пользовательского ввода.


# TODO: добавить репозиторий промокодов
class PromoCodeRepository:

    def __init__(self, connection):
        self.connection= connection 

    def add_promo_code(self, promcod):
        query = """
            INSERT INTO delivery (code, percent, min_total, is_active)
            VALUES (%s, %s, %s, %s)
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (promcod.code, promcod.percent, promcod.min_total, promcod.is_active))

        self.connection.commit()

    def get_promo_code_by_percent(self, percent):
        query = """
            SELECT promcod
            FROM delivery
            WHERE percent = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (percent,)) 
            row = cursor.fetchone()

        if row is None:
            return None

        return PromoCodeRepository(row[0], row[1], row[2], row[3])

# Задание 7
# Создайте сервис скидок.
# Он должен проверять промокод и возвращать сумму после скидки.


# TODO: добавить сервис скидок
class DiscountService:
    def calculate_total(self, total, promcod):
        if promcod is None:
            return total

        if not promcod.is_active:
            raise ValueError("Промокод неактивен")

        if total < promcod.min_total:
            raise ValueError("Сумма меньше минимальной")

        discount = total * promcod.percent // 100
        return total - discount

# Задание 8
# Подключите скидку к оформлению заказа.
# Заказ должен хранить исходную сумму, скидку и итоговую сумму.


# TODO: добавить скидки в заказ


# Задание 9
# Проверьте сценарии: промокод найден, промокод неактивен,
# сумма меньше минимальной, промокод не существует.


# TODO: добавить ручную проверку скидок
