# -*- coding: utf-8 -*-

import pytest
from parser import * 

parser = Parser()

def test_morph1():
	splitted = parser.morphological_split(u'犬の本を')
	assert set(splitted) == set([u'犬+Anim+Gen^本-Anim+Acc'])

def test_morph2():
	splitted = parser.morphological_split(u'犬がいる')
	assert set(splitted) == set([u'犬+Anim+Nom^いる+Anim+Pres'])

def test_morph3():
	splitted = parser.morphological_split(u'あった')
	assert set(splitted) == set([u'ある-Anim+Past'])

def test_parse1():
	parse = parser.parseSentence([u'犬が',u'いる']);
	assert len(parse) >= 1

