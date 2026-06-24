# weather.py

class WeatherObservation:
    """Класс для представления одного погодного наблюдения."""
    def __init__(self, date: str, temperature: float, humidity: float,
                 wind_speed: float, precipitation: float):
        self.date = date
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.precipitation = precipitation

    def __str__(self) -> str:
        return (f"Дата: {self.date}, Температура: {self.temperature}°C, "
                f"Влажность: {self.humidity}%, Ветер: {self.wind_speed} м/с, "
                f"Осадки: {self.precipitation} мм")


class WeatherAnalyzer:
    """Класс для хранения и анализа набора погодных наблюдений."""
    def __init__(self):
        self.observations = []

    def add_observation(self, observation: WeatherObservation) -> None:
        self.observations.append(observation)

    def get_all(self) -> list:
        return self.observations

    def average_temperature(self) -> float | None:
        if not self.observations:
            return None
        return sum(obs.temperature for obs in self.observations) / len(self.observations)

    def hottest_day(self) -> WeatherObservation | None:
        if not self.observations:
            return None
        return max(self.observations, key=lambda obs: obs.temperature)

    def coldest_day(self) -> WeatherObservation | None:
        if not self.observations:
            return None
        return min(self.observations, key=lambda obs: obs.temperature)

    def days_with_precipitation(self) -> list:
        return [obs for obs in self.observations if obs.precipitation > 0]