# -*- coding: utf-8 -*-

#import pytest
from nltk import Tree
from nltk.grammar import FeatStructNonterminal
from parser import * 

parser = Parser()

def test_morph1():
	splitted = parser.morphological_split(u'犬の本を')
	assert set(splitted) == set([u'犬+Anim+Gen+NP^本-Anim+Acc+NP'])

def test_morph2():
	splitted = parser.morphological_split(u'犬がいる')
	assert set(splitted) == set([u'犬+Anim+Nom+NP^\\x.いる(x)-Dobj+Anim-Pass+Pres+V'])

def test_morph3():
	splitted = parser.morphological_split(u'あった')
	assert set(splitted) == set([u'\\x.ある(x)-Dobj-Anim-Pass+Past+V'])

def test_allwords1():
	words = parser.get_all_words(u'犬があった')
	assert set(words) == set([(u'犬+Anim+Nom+NP',u'犬が'), (u'\\x.ある(x)-Dobj-Anim-Pass+Past+V',u'あった')])

def test_allwordsrules1():
	words = [(u'ある-Dobj-Anim-Pass+Past+V',u'あった'), (u'犬+Anim+Nom+NP',u'犬が')]
	assert parser.morphword_pairs_to_rules(words) == u"\n[DOBJ = None,ANIM = False,PASS = False,TENSE = past,*type* = V,PRED = <ある>] -> 'あ' 'っ' 'た'\n[ANIM = True,CASE = nom,*type* = NP,PRED = <犬>] -> '犬' 'が'"

def test_features1():
	assert parser.words_to_rules([u'犬+Anim+Nom+NP',u'いる-Dobj+Anim-Pass+Pres+V']) == (u'\n[ANIM = True,CASE = nom,*type* = NP,PRED = <犬>] -> \'tag1\'\n[DOBJ = None,ANIM = True,PASS = False,TENSE = pres,*type* = V,PRED = <いる>] -> \'tag2\'', [('tag1',u'犬+Anim+Nom+NP'), ('tag2',u'いる-Dobj+Anim-Pass+Pres+V')])

def test_parse1():
	parse = parser.parse_sentence(u'犬+Anim+Nom+NP^いる-Dobj+Anim-Pass+Pres+V');
	assert len(parse) >= 1

def test_morph_parse():
	trees = parser.morph_parse(u'犬の本があった')
	assert len(trees) >= 1
	return (trees, [Tree.fromstring(u"""
		(S[TENSE='past']
			(NP[-ANIM,CASE='nom']
				(NP[+ANIM,CASE='gen',PRED='犬'] 犬+Anim+Gen+NP)
				(NP[-ANIM,CASE='nom',PRED='本'] 本-Anim+Nom+NP))
			(VP[-ANIM,TENSE='past']
				(V[-ANIM,PRED='ある',TENSE='past'] ある-Dboj-Anim+Past+IV)))
		""", read_node=FeatStructNonterminal)])

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
	assert len(p(u'犬が食べる')) >= 1
	#assert len(p(u'安藤先生の本にわかれる')) >= 1
	#assert len(p(u'')) >= 1

def test_nonparsable():
	p = lambda s: list(parser.morph_character_parsing(s))
	assert len(p(u'犬がある')) == 0
	assert len(p(u'本がいる')) == 0
	assert len(p(u'ジョンがある')) == 0
	assert len(p(u'本のある')) == 0
	assert len(p(u'犬がりんごを食べられた')) == 0
	#assert len(p(u'')) == 0

