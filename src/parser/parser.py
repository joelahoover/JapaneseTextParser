# -*- coding: utf-8 -*-

import re
from nltk import FeatStruct, Tree, Variable, grammar, parse
import attapply

grammarText = u"""
%start S
S[TENSE=?t] -> NP[ANIM=?a, CASE=nom] VP[ANIM=?a, TENSE=?t]
NP[ANIM=?a, CASE=?c] -> NP[CASE=gen] NP[ANIM=?a, CASE=?c]
VP[TENSE=?t, ANIM=?a] -> IV[TENSE=?t, ANIM=?a]
"""

featureMap = {
		"+IV": "*type* = IV",
		"+NP": "*type* = NP",
		"+Anim": "ANIM = True",
		"-Anim": "ANIM = False",
		"+Nom": "CASE = nom",
		"+Gen": "CASE = gen",
		"+Dat": "CASE = dat",
		"+Acc": "CASE = acc",
		"+Pres": "TENSE = pres",
		"+Past": "TENSE = past"
}

class Parser(object):
	def __init__(self):
		self.lexicon = attapply.ATTFST('lexicon.fst')
		self.segmenter = attapply.ATTFST('segmenter.fst')
		self.allwords = attapply.ATTFST('allwords.fst')
		self.grammarText = grammarText
		self.tagPrefix = "tag"

	def morphological_split(self, text):
		"""
		Returns a list of the possible morphological analysis for a given string of text.
		"""
		return map(lambda x: x[0], self.segmenter.apply(text, dir = 'up'))

	def get_all_words(self, text):
		"""
		Returns a list of tuples containing all the possible words in the text along with their morphological analysis.
		"""
		morphwords = map(lambda x: x[0], self.allwords.apply(text, dir = 'up'))
		words = []
		for mw in morphwords:
			words.extend(map(lambda x: (mw, x[0]), self.lexicon.apply(mw, dir = 'down')))
		return words

	def words_to_rules(self, words):
		"""
		Returns a tuple contining a string of the grammar rules and a list tuples of tags and words.
		"""
		rules = ""
		tags = []
		count = 0
		for w in words:
			count += 1
			tag = self.tagPrefix + str(count)
			tags.append((tag,w))
			morphfs = list(filter(None, re.split('([+-]?[^+-]+)', w)))
			syntaxfs = [featureMap[f] for f in morphfs[1:]]
			rules += "\n[" + ",".join(syntaxfs + ["PRED = '" + morphfs[0] + "'"]) + "] -> '" + tag + "'"
		return (rules, tags)

	def parse_sentence(self, sentence):
		"""
		Returns a list of the possible parse trees given a sentence.
		"""
		(lexRules, tagWords) = self.words_to_rules(sentence.split('^'))
		g = grammar.FeatureGrammar.fromstring(self.grammarText + lexRules)
		p = parse.FeatureChartParser(g)
		trees = []
		tagWordsDict = dict(tagWords)
		tagWordsVars = dict([ (Variable('?'+x),y) for (x,y) in tagWords ])
		for t in p.parse([t for (t,_) in tagWords]):
			for p in t.treepositions():
				if type(t[p]) == Tree:
					t[p].set_label(t[p].label().substitute_bindings(tagWordsVars))
				else:
					t[p] = tagWordsDict[t[p]]
			trees += [t]
		return trees

	def morph_parse(self, text):
		"""
		Applies morphological analysis to the text and returns all the possible parse trees.
		"""
		sentences = self.morphological_split(text)
		trees = []
		for s in sentences:
			ts = self.parse_sentence(s)
			trees += ts
		return trees

