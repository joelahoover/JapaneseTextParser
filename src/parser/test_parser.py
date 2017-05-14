# -*- coding: utf-8 -*-

#import pytest
from nltk import Tree
from nltk.grammar import FeatStructNonterminal
from parser import * 

parser = Parser()

def test_morph1():
	splitted = parser.morphological_split(u'犬の本を')
	assert set(splitted) == set([u'dog+Anim+Gen+NP^book-Anim+Acc+NP'])

def test_morph2():
	splitted = parser.morphological_split(u'犬がいる')
	assert set(splitted) == set([u'dog+Anim+Nom+NP^\\x.Exists(x)-Dobj+Anim-Vmod+Pres+V'])

def test_morph3():
	splitted = parser.morphological_split(u'あった')
	assert set(splitted) == set([u'\\x.Exists(x)-Dobj-Anim-Vmod+Past+V'])

def test_allwords1():
	words = parser.get_all_words(u'犬があった')
	assert set(words) == set([(u'dog+Anim+Nom+NP',u'犬が'), (u'\\x.Exists(x)-Dobj-Anim-Vmod+Past+V',u'あった')])

def test_allwordsrules1():
	words = [(u'\\x.exists(x)-Dobj-Anim-Vmod+Past+V',u'あった'), (u'dog+Anim+Nom+NP',u'犬が')]
	assert parser.morphword_pairs_to_rules(words) == u"\n[DOBJ = None,ANIM = False,MOD = None,TENSE = past,*type* = V,PRED = <\\x.exists(x)>] -> 'あ' 'っ' 'た'\n[ANIM = True,CASE = nom,*type* = NP,PRED = <dog>] -> '犬' 'が'"

def test_features1():
	assert parser.words_to_rules([u'dog+Anim+Nom+NP',u'\\x.Exists(x)-Dobj+Anim-Vmod+Pres+V']) == (u'\n[ANIM = True,CASE = nom,*type* = NP,PRED = <dog>] -> \'tag1\'\n[DOBJ = None,ANIM = True,MOD = None,TENSE = pres,*type* = V,PRED = <\\x.Exists(x)>] -> \'tag2\'', [('tag1',u'dog+Anim+Nom+NP'), ('tag2',u'\\x.Exists(x)-Dobj+Anim-Vmod+Pres+V')])

def test_parse1():
	parse = parser.parse_sentence(u'dog+Anim+Nom+NP^\\x.Exists(x)-Dobj+Anim-Vmod+Pres+V');
	assert len(parse) >= 1

def test_morph_parse():
	trees = parser.morph_parse(u'犬の本があった')
	assert len(trees) >= 1

def test_parseable():
	p = lambda s: list(parser.morph_character_parsing(s))
	assert len(p(u'本がある')) >= 1
	assert len(p(u'みちこがいる')) >= 1
	assert len(p(u'犬がいる')) >= 1
	assert len(p(u'犬がいた')) >= 1
	assert len(p(u'犬がいます')) >= 1
	assert len(p(u'犬がいました')) >= 1
	assert len(p(u'犬がいません')) >= 1
	assert len(p(u'犬がいませんでした')) >= 1
	assert len(p(u'犬がりんごを食べる')) >= 1
	assert len(p(u'犬がメアリーのラーメンを食べませんでした')) >= 1
	assert len(p(u'りんごが犬に食べられた')) >= 1
	assert len(p(u'本がわかりませんでした')) >= 1
	assert len(p(u'安藤先生の本がわかった')) >= 1
	assert len(p(u'メアリーさんが日本語を話しません')) >= 1
	assert len(p(u'英語が安藤先生に話されます')) >= 1
	assert len(p(u'日本語を話す')) >= 1
	assert len(p(u'犬がりんごが食べられる')) >= 1
	assert len(p(u'犬がりんごを食べられる')) >= 1
	assert len(p(u'犬が日本語を話せます')) >= 1
	assert len(p(u'ジョン君が英語が話せます')) >= 1
	assert len(p(u'安藤先生の本がわかれません')) >= 1
	#assert len(p(u'')) >= 1

def test_nonparsable():
	p = lambda s: list(parser.morph_character_parsing(s))
	assert len(p(u'犬がある')) == 0
	assert len(p(u'本がいる')) == 0
	assert len(p(u'ジョンがある')) == 0
	assert len(p(u'本のある')) == 0
	#assert len(p(u'')) == 0

