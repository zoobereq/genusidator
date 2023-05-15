## Genusidator 🇩🇪 🇦🇹 🇨🇭 
#### A learning aid to explain grammatical gender assignment in German nouns


#### Background
One of the biggest challenges for learners of German is accurately identifying the grammatical gender of German nouns (masculine, feminine, or neuter). Unlike native German speakers who learned the grammatical gender mappings via the process of language acquisition, learners of German as a foreign language are not naturally exposed to the gender of German nouns during the formative period of language development. Moreover, the topic is generally not taught in German schools. As a result, even native German speakers tasked with teaching German to foreigners are rarely able to teach their students how to match nouns to their gender. 


#### Rationale
This program aims to address the above limitation by automatically generating the rules governing grammatical gender assignment. In order to accomplish this task, the system relies on a combination of semantic taxonomic relationships and word morphology. One hopes that by understanding these rules, learners will be able to more confidently use entire categories of nouns with the correct grammatical gender.


#### Technology
Genusidator employs the following technologies:
- [spaCy German transformer pipeline](https://github.com/explosion/spacy-models/releases/tag/de_dep_news_trf-3.5.0) is used for grammatical class detection and lemmatization.
- [Google Translate API](https://pypi.org/project/googletrans/) 
- [German Compound Noun Splitter](https://github.com/repodiac/german_compound_splitter) used to split nominal composita and output the base noun. Note that a dictionary object is required for morphological parsing. Any dictionary with one item per line will do. The present implementation employs [Free German Dictionary](https://sourceforge.net/projects/germandict/files/latest/download) by Jan Schreiber. An abridged version of this resource is included in the repo.
- NLTK and WordNet are used to generate the hypernym taxonomy for each noun
- Monosyllabicity is verified with [Syllables](https://pypi.org/project/syllables/), a package to estimate the number of syllables in English words. It works well detecting monosyllabic German words, however the string needs to be first stransformed to remove the Umlauts and the Eszett.
- Foreign borrowings are detected with the [langdetect](https://pypi.org/project/langdetect/) package.


#### Installation
Installation is easy with `pip` and the built-in `git` package installation protocol:

`pip install git+https://github.com/zoobereq/genusidator`


#### Evaluation
The evaluation is forthcoming.


#### References
The project was inspired by _Der, Die, Das: The Secrets of German Gender_ by Constantin Vayenas (2019).

