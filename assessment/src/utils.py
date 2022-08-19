import re
import unidecode


def remove_accentuation(raw_str):
    return unidecode.unidecode(raw_str.strip())


def normalize_case(raw_str, use_uppercase=False):
    if use_uppercase:
        return raw_str.upper()
    return raw_str.lower()


def normalize_phone_number(raw_str):
    return re.sub(r"[^\d\+]", "", raw_str)


def normalize_spacing(raw_str):
    return " ".join(raw_str.split())
