#!/usr/bin/env python
"""A function generating a noun-restricted taxonomy of hypernyms for the input string"""

import warnings

from nltk.corpus import wordnet as wn

warnings.filterwarnings("ignore")  # discards warnings about redundant hypernym searches


def taxonomy(word: str) -> list:
    all_hypernyms = []
    if wn.synsets(
        word, pos=wn.NOUN
    ):  # checks if there are any synsets to begin with. Proper nouns don't have synsets.
        synsets = wn.synsets(word, pos=wn.NOUN)
        for synset in synsets:
            hypernym_list = []
            hyper = (
                lambda s: s.hypernyms()
            )  # function to iterate up the hypernym taxonomy
            if (
                list(synset.closure(hyper, depth=1)) == synset.hypernyms()
            ):  # validates closure over the hypernym hierarchy
                hypernyms = list(
                    synset.closure(hyper)
                )  # generates a list of hypernym synsets
                for synset in hypernyms:
                    for lemma in synset.lemmas():
                        hypernym_list.append(lemma.name().replace("_", " "))
            all_hypernyms.append(hypernym_list)
        return list(
            set([item for sublist in all_hypernyms for item in sublist])
        )  # flattens the list and removes duplicate categories
