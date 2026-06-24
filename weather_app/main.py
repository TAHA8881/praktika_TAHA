# main.py

from weather import WeatherObservation, WeatherAnalyzer

def input_observation() -> WeatherObservation:
    """Функция ввода данных с проверкой корректности."""
    while True:
        date = input("Введите дату (например, 2026-06-24): ").strip()
        if date:
            break
        print("Дата не может быть пустой.")

    while True:
        try:
            temp = float(input("Введите температуру (в °C): "))
            break
        except ValueError:
            print("Ошибка: введите число.")

    while True:
        try:
            hum = float(input("Введите влажность (0-100%): "))
            if 0 <= hum <= 100:
                break
            print("Влажность должна быть от 0 до 100.")
        except ValueError:
            print("Ошибка: введите число.")

    while True:
        try:
            wind = float(input("Введите скорость ветра (м/с, неотрицательное): "))
            if wind >= 0:
                break
            print("Скорость ветра не может быть отрицательной.")
        except ValueError:
            print("Ошибка: введите число.")

    while True:
        try:
            precip = float(input("Введите количество осадков (мм, неотрицательное): "))
            if precip >= 0:
                break
            print("Осадки не могут быть отрицательными.")
        except ValueError:
            print("Ошибка: введите число.")

    return WeatherObservation(date, temp, hum, wind, precip)


def main():
    analyzer = WeatherAnalyzer()

    # Добавление демонстрационных данных за 5 дней (по условию)
    demo_data = [
        ("2026-06-20", 22.5, 65, 3.2, 0.0),
        ("2026-06-21", 18.0, 80, 5.1, 5.2),
        ("2026-06-22", 25.3, 55, 2.0, 0.0),
        ("2026-06-23", 14.8, 90, 4.5, 12.0),
        ("2026-06-24", 20.0, 70, 3.0, 0.5),
    ]
    for date, temp, hum, wind, precip in demo_data:
        analyzer.add_observation(WeatherObservation(date, temp, hum, wind, precip))

    while True:
        print("\n=== Система анализа погодных наблюдений ===")
        print("1. Добавить наблюдение")
        print("2. Просмотреть все наблюдения")
        print("3. Рассчитать среднюю температуру")
        print("4. Определить самый тёплый день")
        print("5. Определить самый холодный день")
        print("6. Вывести дни с осадками")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "0":
            print("До свидания!")
            break
        elif choice == "1":
            obs = input_observation()
            analyzer.add_observation(obs)
            print("Наблюдение добавлено.")
        elif choice == "2":
            obs_list = analyzer.get_all()
            if not obs_list:
                print("Нет наблюдений.")
            else:
                for i, obs in enumerate(obs_list, 1):
                    print(f"{i}. {obs}")
        elif choice == "3":
            avg = analyzer.average_temperature()
            if avg is None:
                print("Нет данных.")
            else:
                print(f"Средняя температура: {avg:.2f}°C")
        elif choice == "4":
            hottest = analyzer.hottest_day()
            if hottest is None:
                print("Нет данных.")
            else:
                print(f"Самый тёплый день: {hottest}")
        elif choice == "5":
            coldest = analyzer.coldest_day()
            if coldest is None:
                print("Нет данных.")
            else:
                print(f"Самый холодный день: {coldest}")
        elif choice == "6":
            precip_days = analyzer.days_with_precipitation()
            if not precip_days:
                print("Дней с осадками нет.")
            else:
                print("Дни с осадками:")
                for obs in precip_days:
                    print(obs)
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()