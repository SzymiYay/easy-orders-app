import re


def matches_regex(regex: str, text: str) -> bool:
    return re.match(regex, text) is not None


def has_only_upper(text: str) -> bool:
    return matches_regex(r'^([A-Z]+\s?)+$', text)