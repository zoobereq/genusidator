#!/usr/bin/env python

import argparse

import spacy
from googletrans import Translator

from hypernyms import taxonomy

translator = Translator()
nlp = spacy.load(
    "de_core_news_lg"
)  # lemmatizer doesn't work as well when trained on smaller corpora


def main(args: argparse.Namespace) -> None:
    nouns = args.input
    doc = nlp(nouns)
    for noun in doc:
        lemmatized = noun.lemma_  # run it throug the German lemmatizer
        translation = translator.translate(
            lemmatized, src="de", dest="en"
        )  # translate into EN
        translated = translation.text.casefold()
        hypernyms = taxonomy(translated)
        print(hypernyms)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="provide a German noun")
    main(parser.parse_args())
