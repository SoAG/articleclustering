import re, math, ner
from nltk.stem.porter import PorterStemmer

stopwords = ['a', 'about', 'above', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also','although','always','am','among', 'amongst', 'amoungst', 'amount',  'an', 'and', 'another', 'any','anyhow','anyone','anything','anyway', 'anywhere', 'are', 'around', 'as',  'at', 'back','be','became', 'because','become','becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 'between', 'beyond', 'bill', 'both', 'bottom','but', 'by', 'call', 'can', 'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de', 'describe', 'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight', 'either', 'eleven','else', 'elsewhere', 'empty', 'enough', 'etc', 'even', 'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few', 'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former', 'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get', 'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'however', 'hundred', 'ie', 'if', 'in', 'inc', 'indeed', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly', 'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never', 'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own','part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same', 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she', 'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third', 'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well', 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself', 'yourselves', 'the']


		
class Document(object):
	"""Representation of one document. Reads the document and performs normalization of the document (removal of stopwords, stemming, named entity recognition). Terms are kept in a BagOfWords that represents this document."""

	#BagOfWords to keep words of all documents
	vocabulary = None
	#keep occurrence of word in documents
	document_word_frequency = {}
	#number of documents in collection
	number_of_documents = 0.0

	def __init__(self, document):
		super(Document, self).__init__()
		self.content = ""
		self.title = ""
		self.source = ""
		self.published = ""
		self.bag_of_words = BagOfWords()
		self.ner_tagger = ner.SocketNER(host='localhost', port=1239, output_format="slashTags")
		if Document.vocabulary is None:
			Document.vocabulary = BagOfWords()
		self.read_document(document)
		Document.number_of_documents += 1
		self.list_rep = []

	def read_document(self, document):
		"""Read document from json and save contained information."""
		self.content = document['content']
		self.title = document['title']
		self.source = document['source_url']
		self.published = document['published']
		self.create_bag_of_words()
		# self.clean_document_vocabulary()


	def create_bag_of_words(self):
		"""Create a BagOfWords for the document. Performs named entity recognition, stemming and stopword removal. """
		stemmer = PorterStemmer()
		nes = []
		tagged_text = self.ner_tagger.get_entities(self.content.encode('utf-8'))
		for key in tagged_text.keys():
			if key != 'O':
				nes += tagged_text[key]
		for n in nes:
			self.bag_of_words.add_stem_word(n, n)
			Document.vocabulary.add_stem_word(n, n)

		wo_named = re.sub('|'.join(nes), '', self.content)

		words = re.findall(r'\w+', wo_named,flags = re.UNICODE | re.LOCALE) 
		for wordo in words:
			word = wordo.rstrip(r'\n')
			if word.lower() not in stopwords:
				w = stemmer.stem(word.lower())
				self.bag_of_words.add_stem_word(w, word)
				Document.vocabulary.add_stem_word(w, word)

		for word in self.bag_of_words.get_all_words():
			if word in Document.document_word_frequency:
				Document.document_word_frequency[word] += 1
			else:
				Document.document_word_frequency[word] = 1

	def set_list_rep(self, l):
		self.list_rep = l
				


	def stats(self):
		self.bag_of_words.stats()
		Document.vocabulary.stats()
		

class BagOfWords(object):
	"""BagOfWords representation for a document. Keeps occurrence of each word in a document."""
	def __init__(self):
		super(BagOfWords, self).__init__()
		self.words = {}
		self.number_of_words = 0
		self.stem_word_map = {}
		self.topic_terms = []

	def add_stem_word(self, stem, word):
		"""Add a word to the BagOfWords. The stem of the word is used for the frequency but also the original word is kept and mapped to the stem."""
		self.number_of_words += 1
		if stem.lower() in self.words:
			self.words[stem.lower()] += 1
		else:
			self.words[stem.lower()] = 1
		if stem.lower() in self.stem_word_map:
			if word.lower() not in self.stem_word_map[stem.lower()]:
				self.stem_word_map[stem.lower()].append(word.lower())
		else:
			self.stem_word_map[stem.lower()] = [word.lower()]


	def len(self):
		"""Number of words contained in this BagOfWords."""
		return len(self.words)

	def get_all_words(self):
		"""Get all words contained in the BagOfWords"""
		return self.words.keys()

	def get_word_freq(self, word):
		"""Get the frequency of a specific word."""
		if word in self.words:
			return self.words[word]
		else:
			return 0

	def get_word_index(self, word):
		"""Get the index of a word"""
		return self.words.keys().index(word)

	def get_bag_as_list(self):
		"""Get the frequency of each word as a list."""
		ls = []
		for word in Document.vocabulary.get_all_words():
			ls.append(self.get_word_freq(word))
		return ls

	def get_word_by_index(self, index):
		"""Get word by index."""
		return self.words.keys()[index]

	def get_tf_idf(self):
		"""Get TFIDF values as a list."""
		tf_idf = []
		for w in Document.vocabulary.get_all_words():
			idf = math.log(Document.number_of_documents/Document.document_word_frequency[w])
			tf = self.get_word_freq(w)
			w = tf*idf
			tf_idf.append(w)
		return tf_idf

	def get_stem_word_mapping(self, index):
		"""Get original list of words for a stemmed word in the BagOfWords"""
		return self.stem_word_map.values()[index]

	def add_importance_to_word(self, word):
		"""Give a word more weight (only used for terms that define a topic)"""
		if word in self.words:
			self.words[word] += self.words[word]*3
			if word not in self.topic_terms:
				self.topic_terms.append(word)

	def stats(self):
		"""print some statistics about this BagOfWords"""
		print self.len()
		print self.words



