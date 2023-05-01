#!/usr/bin/env python
"""A function that generates a noun-restricted taxonomy of hypernyms for the input string"""

from nltk.corpus import wordnet as wn


def taxonomy(word: str) -> list:
    hypernym_list = []
    if wn.synsets(word, pos=wn.NOUN):
        target = wn.synsets(word, pos=wn.NOUN)[
            0
        ]  # generate the meaning (assume the first synset is the default)
        hyper = lambda s: s.hypernyms()  # function to iterate up the hypernym taxonomy
        if (
            list(target.closure(hyper, depth=1)) == target.hypernyms()
        ):  # validate closure overthe hypernym hierarchy
            hypernyms = list(
                target.closure(hyper)
            )  # generate a list of hypernym synsets
            for synset in hypernyms:
                for lemma in synset.lemmas():
                    hypernym_list.append(lemma.name().replace("_", " "))
        return hypernym_list
    else:
        return "There are no synsets available for this word."
