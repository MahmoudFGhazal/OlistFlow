

import unicodedata


def normalize_city(city: str) -> str:
    if not isinstance(city, str):
        return city

    city = city.strip().lower()

    return ''.join(
        char
        for char in unicodedata.normalize('NFKD', city)
        if not unicodedata.combining(char)
    )