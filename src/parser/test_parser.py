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
	assert set(splitted) == set([u'犬+Anim+Nom+NP^いる+Anim+Pres+IV'])

def test_morph3():
	splitted = parser.morphological_split(u'あった')
	assert set(splitted) == set([u'ある-Anim+Past+IV'])

def test_allwords1():
	words = parser.get_all_words(u'犬があった')
	assert set(words) == set([(u'犬+Anim+Nom+NP',u'犬が'), (u'ある-Anim+Past+IV',u'あった')])

def test_features1():
	assert parser.words_to_rules([u'犬+Anim+Nom+NP',u'いる+Anim+Pres+IV']) == (u'\n[ANIM = True,CASE = nom,*type* = NP,PRED = \'犬\'] -> \'tag1\'\n[ANIM = True,TENSE = pres,*type* = IV,PRED = \'いる\'] -> \'tag2\'', [('tag1',u'犬+Anim+Nom+NP'), ('tag2',u'いる+Anim+Pres+IV')])

def test_parse1():
	parse = parser.parse_sentence(u'犬+Anim+Nom+NP^いる+Anim+Pres+IV');
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
				(IV[-ANIM,PRED='ある',TENSE='past'] ある-Anim+Past+IV)))
		""", read_node=FeatStructNonterminal)])

