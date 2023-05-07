#!/usr/bin/env python

import argparse

import spacy
from googletrans import Translator

from der import masc_evaluate
from die import fem_evaluate
from das import neut_evaluate
from hypernyms import taxonomy

# de_nouns = Nouns()
translator = Translator()
nlp = spacy.load(
    "de_core_news_lg"
)  # the lemmatizer doesn't work as well when trained on smaller corpora


def main(args: argparse.Namespace) -> None:
    nouns = args.input
    doc = nlp(nouns)
    for noun in doc:
        gender = noun.morph.get("Gender")  # retrieve the correct grammatical gender
        lemmatized = noun.lemma_  # run the noun throug the German lemmatizer
        translation = translator.translate(
            lemmatized, src="de", dest="en"
        )  # translate from DE into EN to traverse WordNet
        translated = translation.text.casefold()  # casefold the EN translation string
        hypernyms = taxonomy(translated)  # generate all possible hypernyms

        # Run the masculine tests
        if gender == ["Masc"]:
            masc_evaluate(lemmatized, hypernyms)
        
        # Run the feminine test
        elif gender == ["Fem"]:
            fem_evaluate(lemmatized, hypernyms)

        # Run the neuter test
        else:
            neut_evaluate(lemmatized, hypernyms)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="provide a German noun")
    main(parser.parse_args())
