import re

def valid_phone(phone):
    return bool(re.fullmatch(r"\d{10}", phone))

def strong_password(password):
    if len(password) < 6:
        return False

    if not re.search(r"[A-Za-z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    return True