from typing import List

EMPTY_PHONES = ['sil', 'spn', 'eps', '$0']


def clean_phones(phones: List[str]) -> List[str]:
    ret = [p for p in phones if p.isalnum()]
    ret = [p for p in ret if p.lower() not in EMPTY_PHONES]
    return ret
