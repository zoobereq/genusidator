#!/usr/bin/env python
"""a module to split up German compound words based on a user-defined external German dictionary and a an implementation of the Aho-Corasick algorithm for multi-pattern string search and retrieval. Attribution:  german_compound_splitter, Copyright 2020 by repodiac, see https://github.com/repodiac for updates and further information.
"""

from german_compound_splitter import comp_split


def parser(noun: str, ahocs) -> list:
    parsed = comp_split.dissect(noun, ahocs, make_singular=True)
    return parsed
