# -*- coding: utf-8 -*-

import re
from nltk import FeatStruct, Tree, Variable, grammar, parse
import attapply

grammarText = u"""
%start S
S[TENSE=?t] -> NP[ANIM=?a, CASE=nom] VP[ANIM=?a, TENSE=?t]
NP[ANIM=?a, CASE=?c] -> NP[CASE=gen] NP[ANIM=?a, CASE=?c]
VP[TENSE=?t, ANIM=?a] -> V[TENSE=?t, ANIM=?a, DOBJ=None]
VP[TENSE=?t, ANIM=?a] -> NP[CASE=?c] V[TENSE=?t, ANIM=?a, DOBJ=?c]
"""

featureMap = {
		"+V": "*type* = V",
		"+NP": "*type* = NP",
		"+Anim": "ANIM = True",
		"-Anim": "ANIM = False",
		"+Nom": "CASE = nom",
		"+Gen": "CASE = gen",
		"+Dat": "CASE = dat",
		"+Acc": "CASE = acc",
		"+Pres": "TENSE = pres",
		"+Past": "TENSE = past",
		"+Dobj": "DOBJ = acc"
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

	def morphword_pairs_to_rules(self, word_pairs):
		"""
		Returns a sting containing the rules that recognize a sequence of characters into the given words.
		"""
		rules = ""
		for (mw, w) in word_pairs:
			morphfs = list(filter(None, re.split('([+-]?[^+-]+)', mw)))
			syntaxfs = [featureMap[f] for f in morphfs[1:]]
			rules += "\n[" + ",".join(syntaxfs + ["PRED = '" + morphfs[0] + "'"]) + "] -> '" + "' '".join(w) + "'"
		return rules

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

	def morph_character_parsing(self, text):
		"""
		Extracts the words from the text, performs morphological analysis on the words, and then parses the text character by character.
		"""
		lexRules = self.morphword_pairs_to_rules(self.get_all_words(text))
		g = grammar.FeatureGrammar.fromstring(self.grammarText + lexRules)
		p =  parse.FeatureChartParser(g)
		return p.parse(text)

	def showParse(self, text):
		trees = list(self.morph_character_parsing(text))
		print(trees)
		for t in trees:
			t.draw()

