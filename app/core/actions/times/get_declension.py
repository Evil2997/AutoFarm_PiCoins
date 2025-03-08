def get_declension(number: int, forms: list[str]) -> str:
    if 11 <= number % 100 <= 14:
        return forms[2]
    elif number % 10 == 1:
        return forms[0]
    elif 2 <= number % 10 <= 4:
        return forms[1]
    else:
        return forms[2]
