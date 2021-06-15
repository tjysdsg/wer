import regex
from typing import List

EMPTY_PHONES = ['sil', 'spn', 'eps', '$0']
phone_pat = r'[A-Za-z0-9_]+'
phone_matcher = regex.compile(phone_pat)


def clean_phones(phones: List[str]) -> List[str]:
    ret = [p for p in phones if phone_matcher.search(p)]
    ret = [p for p in ret if p.lower() not in EMPTY_PHONES]
    return ret
