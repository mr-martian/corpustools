# corpustools
Scripts for dealing with Apertium Stream Format

# goal

Eventually be able to write things like

```
# print lines beginning with a definite determiner followed by a plural noun
cat corpus.txt | apertium eng-tagger | query.py -t 'line(word(<det><def>*) word(<n><pl>))'

# print LUs with 3 or more readings
cat corpus.txt | apertium eng-morph | query.py -m 'word(len(readings) > 2)'
