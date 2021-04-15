from .converter import convert


def celsius_to_fahrenheit(celsius_temperature):
    """Convert Celsius to Fahrenheit."""
    return convert(celsius_temperature, 'degC', 'degF')


def celsius_to_kelvin(celsius_temperature):
    """Convert Celsius to Kelvin."""
    return convert(celsius_temperature, 'degC', 'kelvin')


def fahrenheit_to_celsius(fahrenheit_temperature):
    """Convert Fahrenheit to Celsius."""
    return convert(fahrenheit_temperature, 'degF', 'degC')


def fahrenheit_to_kelvin(fahrenheit_temperature):
    """Convert Fahrenheit to Kelvin."""
    return convert(fahrenheit_temperature, 'degF', 'kelvin')


def kelvin_to_celsius(kelvin_temperature):
    """Convert Kelvin to Celsius."""
    return convert(kelvin_temperature, 'kelvin', 'degC')


def kelvin_to_fahrenheit(kelvin_temperature):
    """Convert Kelvin to Fahrenheit."""
    return convert(kelvin_temperature, 'kelvin', 'degF')


def celsius_to_felsius(celsius_temperature):
    """Convert the celsius_temperature into the Felsius temperature (see https://xkcd.com/1923/)."""
    import statistics

    fahrenheit_temperature = celsius_to_fahrenheit(celsius_temperature)
    felsius_temperature = statistics.mean([celsius_temperature, fahrenheit_temperature])

    return felsius_temperature


def fahrenheit_to_felsius(fahrenheit_temperature):
    """Convert the fahrenheit_temperature into the Felsius temperature (see https://xkcd.com/1923/)."""
    import statistics

    celsius_temperature = fahrenheit_to_celsius(fahrenheit_temperature)
    felsius_temperature = statistics.mean([celsius_temperature, fahrenheit_temperature])

    return felsius_temperature


def kelvin_to_felsius(kelvin_temperature):
    """Convert the kelvin_temperature into the Felsius temperature (see https://xkcd.com/1923/)."""
    fahrenheit_temperature = kelvin_to_fahrenheit(kelvin_temperature)
    import statistics

    celsius_temperature = kelvin_to_celsius(kelvin_temperature)
    felsius_temperature = statistics.mean([celsius_temperature, fahrenheit_temperature])

    return felsius_temperature
