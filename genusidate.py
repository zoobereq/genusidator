#!/usr/bin/env python

import argparse
import spacy
import wn
import googletrans
from nltk.corpus import wordnet as wn
# from odenet import *


#from google_trans_new import google_translator
from googletrans import Translator
translator = Translator()



#wn.download('odenet')
#wn.download('oewn')
#de = wn.Wordnet('odenet')
#en = wn.Wordnet('oewn')
nlp = spacy.load("de_core_news_lg") # lemmatizer doesn't work as well on smaller corpora

nouns = "Katze"

def main() -> None:
    doc = nlp(nouns)
    for noun in doc:
        lemmatized = noun.lemma_
        translation = translator.translate(lemmatized, src='de', dest='en')
        translation.text
        target_word = wn.synset(translation.text)[0]
        print(target_word.hyperhyms())
        
        #word = de.senses(lemmatized)[0]
        #en_senses = word.senses()[0].translate(lexicon='oewn')
        #print(word)
        #print([s.word().lemma() for s in en_senses])

"""
word = de.synsets(lemmatized, pos='n')[0]
hypernyms = word.hypernyms()
for hypernym in hypernyms:
    print(hypernym.words())
"""
        


        


# def main(args: argparse.Namespace) -> None:
#     pass


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description=__doc__)
    # parser.add_argument("--input", help="provide a German noun")
    # main(parser.parse_args())
    main()
