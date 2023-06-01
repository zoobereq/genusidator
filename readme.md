## Genusidator 🇩🇪 🇦🇹 🇨🇭 
#### A learning aid to explain grammatical gender assignment in German nouns


#### Background
One of the biggest challenges for learners of German is accurately identifying the grammatical gender of German nouns (masculine, feminine, or neuter). Unlike native German speakers who learned the grammatical gender mappings via the process of language acquisition, learners of German as a foreign language are not naturally exposed to the gender of German nouns during the formative period of language development. Moreover, the topic is generally not taught in German schools. As a result, even native German speakers tasked with teaching German to foreigners are rarely able to teach their students how to match nouns to their gender. 


#### Rationale
This program aims to address the above limitation by automatically generating the rules governing grammatical gender assignment. In order to accomplish this task, the system relies on a combination of semantic taxonomic relationships and word morphology. One hopes that by understanding these rules, learners will be able to more confidently use entire categories of nouns with the correct grammatical gender.


#### Technology
Genusidator employs the following technologies:
- [spaCy German transformer pipeline](https://github.com/explosion/spacy-models/releases/tag/de_dep_news_trf-3.5.0) is used for grammatical class detection and lemmatization.
- [DeepL API](https://pypi.org/project/googletrans/) is used to output US-English translation. The translation both helps furnish semantic context and is required to generate a hypernm taxonomy. Make sure to supply your own DeepL API key, which can be obtained [here](https://www.deepl.com/pro-api?cta=header-pro-api). The earlier versions of this program implemented the Google Translate API, which proved much less reliable and accurate than DeepL.
- [German Compound Noun Splitter](https://github.com/repodiac/german_compound_splitter) is used to split nominal composita and output the base noun. Note that a dictionary object is required for morphological parsing. Any dictionary with one item per line will do. The present implementation employs [Free German Dictionary](https://sourceforge.net/projects/germandict/files/latest/download) by Jan Schreiber. An abridged version of this resource is included in the repo.
- NLTK and WordNet are used to generate the hypernym taxonomy for each noun
- Monosyllabicity is verified with [Syllables](https://pypi.org/project/syllables/), a package to estimate the number of syllables in English words. It works well detecting monosyllabic German words, however the string needs to be first stransformed to remove the Umlauts and the Eszett.
- Foreign borrowings are detected with the [langdetect](https://pypi.org/project/langdetect/) package.


#### Evaluation
In order to evaluate the system a list of 102,444 German nouns was extracted from [this list](https://pypi.org/project/german-nouns/). After removing the duplicates 100064 nouns remained. All lemmas were analyzed for the grammatical gender with the spaCy pipeline, of which 90623 nouns were successfully morphologically identified. The identified nouns represented the following grammatical classes:
- 32164 were masculine
- 36306 were feminine
- 22153 were neuter

Four feature sets were extracted (semantic, morphological, etymological, and syllabic/phonological) and employed in training a multinomial lgistic regression classifier
The baseline accuracy of the model is 0.396, which reflects the imbalanced ratio between the three genders. Below are the accuracy scores for each feature set, followed by the accuracy for all the features combined:

- Semantic features:                0.419
- Morphological features:           0.750
- Etymological features:            0.405
- Syllabic/phonological features:   0.405
- **All featires combined:          0.752**   


#### References
The project was inspired by _Der, Die, Das: The Secrets of German Gender_ by Constantin Vayenas (2019).

