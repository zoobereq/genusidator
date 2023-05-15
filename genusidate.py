#!/usr/bin/env python

import argparse

import spacy
from german_compound_splitter import comp_split
from googletrans import Translator

from compound_parser import compound_base
from das import neut_evaluate
from der import masc_evaluate
from die import fem_evaluate
from hypernyms import taxonomy

"""load a dictionary object for morphological parsing. Any dictionary with one item per line will do.
The present implementation employs Free German Dictionary by Jan Schreiber (https://sourceforge.net/projects/germandict/files/latest/download).
Note: the Free German Dictionary needs to be saved as UTF8 and with Unix/Linux line breaks.  Use the following bash script:
iconv -f ISO_8859-15 german.dic > german_utf8_linux.dic
"""

dictionary = "german_utf8_linux.dic"
ahocs = comp_split.read_dictionary_from_file(
    dictionary
)  # create an object for multi-pattern string search
translator = Translator()
nlp = spacy.load(
    "de_dep_news_trf"
)  # use a transformer pipeline for lemmatizing and noun class extraction


def main(args: argparse.Namespace) -> None:
    nouns = args.input
    doc = nlp(nouns)
    for noun in doc:
        gender = noun.morph.get("Gender")  # retrieve the grammatical gender
        lemmatized = noun.lemma_  # run the noun throug the German lemmatizer
        parsed_base = compound_base(
            lemmatized, ahocs
        )  # parse the compound noun and return its base
        translation = translator.translate(
            lemmatized, src="de", dest="en"
        )  # translate from DE into EN to traverse WordNet
        translated = translation.text.casefold()  # casefold the EN translation string
        hypernyms = taxonomy(
            translated
        )  # generate all possible hypernyms across all available synsets at each taxonomical level

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
