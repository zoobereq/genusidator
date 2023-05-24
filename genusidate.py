#!/usr/bin/env python

import argparse
import os

import deepl
import spacy
from german_compound_splitter import comp_split

from compound_parser import compound_base
from das import neut_evaluate
from der import masc_evaluate
from die import fem_evaluate
from hypernyms import taxonomy

"""load a dictionary object for morphological parsing. Any dictionary with one item per line will do. 
The present implementation employs Free German Dictionary by Jan Schreiber (https://sourceforge.net/projects/germandict/files/latest/download).
An abridged file is included in the repo.
"""

os.environ[
    "TOKENIZERS_PARALLELISM"
] = "false"  # handles the warning displayed when multiprocessing is initiated
dictionary = "german_utf8_linux.dic"  # UTF8 with Linux-style line breaks
ahocs = comp_split.read_dictionary_from_file(
    dictionary
)  # create an object for multi-pattern string search
license_key = "#"  # replace with your own DeepL licence key
deepl_translator = deepl.Translator(license_key)
nlp = spacy.load(
    "de_dep_news_trf"
)  # use a transformer pipeline for lemmatizing and noun class extraction


def main(args: argparse.Namespace) -> None:
    nouns = args.input
    doc = nlp(nouns)
    for noun in doc:
        gender = noun.morph.get("Gender")  # retrieve the grammatical gender
        lemmatized = noun.lemma_  # retrieve the lemmatized form
        parsed_base = compound_base(
            lemmatized, ahocs
        )  # parse the compound noun and return its base
        translation = deepl_translator.translate_text(
            lemmatized, source_lang="DE", target_lang="EN-US"
        )  # translate from DE into EN
        translated = translation.text.casefold()  # casefold the translated EN string
        hypernyms = taxonomy(
            translated
        )  # generate all possible hypernyms across all available synsets at each taxonomical level all the way to the root

        print(f"Most probable English translation: '{translated}'")

        # evaluate for the masculine class
        if gender == ["Masc"]:
            masc_evaluate(lemmatized, hypernyms, parsed_base)

        # evaluate for the feminine class
        elif gender == ["Fem"]:
            fem_evaluate(lemmatized, hypernyms, parsed_base)

        # evaluate for the neuter class
        else:
            neut_evaluate(lemmatized, hypernyms, parsed_base)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="provide a German noun")
    main(parser.parse_args())
