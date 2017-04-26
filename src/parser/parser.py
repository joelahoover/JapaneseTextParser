# -*- coding: utf-8 -*-

import attapply
from nltk import FeatStruct, grammar, parse

grammarText = """
%start S
# S expansion productions
S -> NP[ANIM=?n, CASE='Nom'] VP[ANIM=?n]
# NP expansion productions
NP[ANIM=?n, CASE=?c] -> NP[CASE='Gen'] NP[ANIM=?n, CASE=?c]
# VP expansion productions
VP[TENSE=?t, ANIM=?n] -> IV[TENSE=?t, ANIM=?n]
# Lexicon
NP[CASE='Nom', +ANIM] -> '犬が'
IV[TENSE='Pres', +ANIM] -> 'いる'
IV[TENSE='Pres', -ANIM] -> 'ある'
"""

class Parser(object):
	def __init__(self):
		self.lexicon = attapply.ATTFST('lexicon.fst')
		self.grammarText = grammarText

	def morphological_split(self, text):
		"""
		Returns a list of the possible morphological analysis for a given string of text.
		"""
		return map(lambda (x,_): x, self.lexicon.apply(text, dir = 'up'))

	def parseSentence(self, sentence):
		"""
		Returns a list of the possible parse trees given a sentence.
		"""
		g = grammar.FeatureGrammar.fromstring(self.grammarText, encoding='utf8')
		p = parse.FeatureEarleyChartParser(g)
		return list(p.parse(sentence))

