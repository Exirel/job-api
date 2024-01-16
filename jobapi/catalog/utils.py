"""Utility functions."""
import unicodedata

import unidecode


def normalize(text: str) -> str:
    """Normalize a string.

    The goal is to get a string with non-ascii unicode characters and to get
    only ascii characters. Similar unicode characters will be normalized to
    the NFKC form, and non-ascii characters will be normalized to their
    equivalent ascii characters, e.g. ``é`` becoming ``e``.
    """
    return unidecode.unidecode(
        unicodedata.normalize('NFKC', text)
    )
