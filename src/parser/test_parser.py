# -*- coding: utf-8 -*-

import pytest
from parser import * 

parser = Parser()

def test_morph1():
	splitted = parser.morphological_split(u'本を')
	assert set(splitted) == set([u'本-Anim+Acc'])

