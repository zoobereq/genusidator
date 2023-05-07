#!/usr/bin/env python
"""A module applying semantic, morphological, and phonological criteria to explain the masculine gender assignment"""

import syllables
from german_nouns.lookup import Nouns
from googletrans import Translator

from hypernyms import taxonomy
from rules import masc_classes, masc_prefixes, masc_suffixes

de_nouns = Nouns()
translator = Translator()


def masc_rule1(hypernyms: list) -> list:
    """returns an intersection of the semantic categories associated with the masculine noun class and the set of hypernyms generated by the input noun"""
    categories = []
    for category in hypernyms:
        if category in masc_classes:
            categories.append(category)
    return categories


def masc_rule2(token: str) -> list:
    """checks the input noun for the prefixes and suffixes associated with the masculine noun class"""
    suffixes = []
    prefixes = []
    for suffix in masc_suffixes:
        if token.endswith(suffix):
            suffixes.append("-" + suffix)
    for prefix in masc_prefixes:
        if token.startswith(prefix):
            prefixes.append(prefix + "-")
    return max(suffixes, key=len) + prefixes


def masc_syllables(token: str) -> bool:
    """monosyllabic words in DE are overwhelmingly masculine.  This function estimates the number of syllables in a word.
    The 'syllables' package used here was written for EN lexemes, but due to the phonological similarity between EN and DE it works verly well in detecting
     monosyllabic DE words.  """
    if syllables.estimate(token) == 1:
        return True


def masc_evaluate(lemmatized: str, hypernyms: list) -> None:
    """the fucntion takes the noun and a set of hypernyms generated over all nominal synsets and determines if any of the hypernyms are affiliated with the masculine noun class.  It then performs simple morphological analysis by checking if the noun contains the prefixes and suffixes associated with the masculine gender."""
    masc_flag = False
    print(f"The noun '{lemmatized}' is masculine.")
    # check the semantic taxonomy
    if hypernyms:
        semantic = masc_rule1(hypernyms)
        if semantic:
            print(
                f"It belongs to the following predominantly masculine semantic categories: {', '.join(semantic)}"
            )
            masc_flag = True
        else:
            print(
                "Grammatical gender assignment could not be determined based on the semantic category."
            )
    elif not hypernyms:
        parsed = de_nouns.parse_compound(lemmatized)
        base = parsed[-1]
        parsed_translation = translator.translate(base, src="de", dest="en")
        translated_base = parsed_translation.text.casefold()
        base_hypernyms = taxonomy(translated_base)  # generate all possible hypernyms
        base_semantic = masc_rule1(base_hypernyms)
        if base_semantic:
            print(
                f"Couldn't find any semantic categories for '{lemmatized}'. The base noun '{base}' belongs to the following predominantly masculine semantic categories: {', '.join(base_semantic)}"
            )
            masc_flag = True
        else:
            print(
                f"Couldn't find any semantic categories for '{lemmatized}'. There are no predomiantly masculine semantic categories to which the base noun '{base}' blelongs."
            )
    # check the morphology
    morphological = masc_rule2(lemmatized)
    if morphological:
        print(
            f"The noun has the following masculine affixes: {', '.join(morphological)}"
        )
        masc_flag = True
    else:
        print(
            "Grammatical gender assignment cannot be determined based on the noun's morphology."
        )
    # check if monosyllabic
    monosyllabic = masc_syllables(lemmatized)
    if monosyllabic:
        print(
            f"Monosyllabic nouns are overwhelmingly masculine. '{lemmatized}' is monosyllabic."
        )
        masc_flag = True
    # print this if none of the above applies
    if masc_flag == False:
        print(
            f"The grammatical gender of '{lemmatized}' cannot be explained with the available rules."
        )
        print("For better or worse, it has to be memorized")
