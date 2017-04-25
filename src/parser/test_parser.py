
import pytest
from parser import * 

parser = Parser()

def test_morph1():
	splitted = parser.morphological_split(u'bbbaa')
	assert set(splitted) == set([u'bbbaa', u'bcbaa'])

