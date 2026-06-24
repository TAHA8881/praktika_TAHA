import pytest
from weather import WeatherObservation, WeatherAnalyzer

def test_observation_creation():
    obs = WeatherObservation("2026-06-24", 22.5, 65, 3.2, 0.0)
    assert obs.date == "2026-06-24"
    assert obs.temperature == 22.5
    assert obs.humidity == 65
    assert obs.wind_speed == 3.2
    assert obs.precipitation == 0.0

def test_add_and_get_all():
    analyzer = WeatherAnalyzer()
    obs1 = WeatherObservation("2026-06-20", 22.5, 65, 3.2, 0.0)
    obs2 = WeatherObservation("2026-06-21", 18.0, 80, 5.1, 5.2)
    analyzer.add_observation(obs1)
    analyzer.add_observation(obs2)
    all_obs = analyzer.get_all()
    assert len(all_obs) == 2
    assert all_obs[0] is obs1

def test_average_temperature():
    analyzer = WeatherAnalyzer()
    analyzer.add_observation(WeatherObservation("2026-06-20", 22.5, 65, 3.2, 0.0))
    analyzer.add_observation(WeatherObservation("2026-06-21", 18.0, 80, 5.1, 5.2))
    analyzer.add_observation(WeatherObservation("2026-06-22", 25.3, 55, 2.0, 0.0))
    avg = analyzer.average_temperature()
    assert avg == pytest.approx((22.5 + 18.0 + 25.3) / 3, 0.01)

def test_average_empty():
    analyzer = WeatherAnalyzer()
    assert analyzer.average_temperature() is None

def test_hottest_day():
    analyzer = WeatherAnalyzer()
    obs1 = WeatherObservation("2026-06-20", 22.5, 65, 3.2, 0.0)
    obs2 = WeatherObservation("2026-06-21", 30.0, 70, 4.0, 0.0)
    obs3 = WeatherObservation("2026-06-22", 18.0, 80, 5.0, 10.0)
    analyzer.add_observation(obs1)
    analyzer.add_observation(obs2)
    analyzer.add_observation(obs3)
    assert analyzer.hottest_day() is obs2

def test_coldest_day():
    analyzer = WeatherAnalyzer()
    obs1 = WeatherObservation("2026-06-20", 22.5, 65, 3.2, 0.0)
    obs2 = WeatherObservation("2026-06-21", 30.0, 70, 4.0, 0.0)
    obs3 = WeatherObservation("2026-06-22", 18.0, 80, 5.0, 10.0)
    analyzer.add_observation(obs1)
    analyzer.add_observation(obs2)
    analyzer.add_observation(obs3)
    assert analyzer.coldest_day() is obs3

def test_days_with_precipitation():
    analyzer = WeatherAnalyzer()
    obs1 = WeatherObservation("2026-06-20", 22.5, 65, 3.2, 0.0)
    obs2 = WeatherObservation("2026-06-21", 18.0, 80, 5.1, 5.2)
    obs3 = WeatherObservation("2026-06-22", 25.3, 55, 2.0, 0.0)
    analyzer.add_observation(obs1)
    analyzer.add_observation(obs2)
    analyzer.add_observation(obs3)
    precip_days = analyzer.days_with_precipitation()
    assert len(precip_days) == 1
    assert precip_days[0] is obs2

def test_no_precipitation():
    analyzer = WeatherAnalyzer()
    obs = WeatherObservation("2026-06-20", 22.5, 65, 3.2, 0.0)
    analyzer.add_observation(obs)
    assert analyzer.days_with_precipitation() == []

def test_hottest_empty():
    analyzer = WeatherAnalyzer()
    assert analyzer.hottest_day() is None

def test_coldest_empty():
    analyzer = WeatherAnalyzer()
    assert analyzer.coldest_day() is None