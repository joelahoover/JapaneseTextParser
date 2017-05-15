Japanese Text Parser (JTP)
============================

This poject is a basic morphological, syntactic, and semantic parser for Japanese. This was created as a final project for LING4424 (Computational Linguistics) at Cornell University.

Copyright © Joel Hoover (jah552@cornell.edu)

Building
----------

Both [NLTK](http://www.nltk.org/) and [Foma](https://fomafst.github.io/) must be installed on the system in order to build.

To build, simply go to the root of the project directory and run `make` or `make all`. To verify the system was built and is working correctly, run `make test`.

Usage
-------

To run the system, run `make run`. This will open up a python interpreter with the parser already loaded into an object called `p`. Then, try parsing one of the sentences below or try your own sentence!

```
p.showParse(u'りんごがメアリーちゃんに食べられた')
p.showParse(u'犬が日本語が話せません')
p.showParse(u'世の中がわかります')
p.showParse(u'英語が安藤先生に話されます')
```
