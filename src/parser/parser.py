
import attapply

class Parser(object):
	def __init__(self):
		self.lexicon = attapply.ATTFST('lexicon.fst')

	def morphological_split(self, text):
		"""
		Returns a list of the possible morphological analysis for a given string of text.
		"""
		return map(lambda (x,_): x, self.lexicon.apply(text, dir = 'down'))


