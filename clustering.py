from numpy import *
from  documentrep import Document
import numpy

class Clusterer(object):
	"""HierarchicalClusterer to cluster documents. Four different fusion functions are supported (single_linkage, complete_linkage, average_linkage, average_group_linkage). Also extracts topics form documents."""

	def __init__(self, documents, distance, iterations=100000):
		super(Clusterer, self).__init__()
		self.documents = documents
		self.dist_matrix = []
		self.clusters = []
		self.distance = distance
		self.topics = []
		self.number_of_iterations = iterations

	def clean_topics(self, topics, T):
		"""clean extracted topics accoring to the T matrix obtained by SVD. If terms do not correlate according to the T matrix a new topic for these terms is created."""
		con = topics[0:len(topics)]
		cleaned_topics = []
		for i in range(len(con)):
			for j in range(i+1, len(con)):
				samecon = []
				samei = []
				if j != i:
					for c1 in con[i]:
						for c2 in con[j]:
							if c1 == c2:
								samecon.append(c2)
								samei.append(Document.vocabulary.get_word_index(c2))
					tmp = []
					tmp1 = []
					if float(len(samecon))/(len(con[i])) >= 0.3:
						c1wordi = []
						for c1 in con[i]:
							if c1 not in samecon:
								c1wordi.append(Document.vocabulary.get_word_index(c1))
								tmp.append(c1)
						c2wordi = []
						for c2 in con[j]:
							if c2 not in samecon:
								c2wordi.append(Document.vocabulary.get_word_index(c2))
								tmp1.append(c2)

						size = min(len(c2wordi), len(c1wordi))
						sumd = 0.0
						sums = 0.0

						for x in range(size):
							sumd += T[c1wordi[x], c2wordi[x]]
						newconcept = []
						sumd = sumd/size
						if sumd < 0.5:
							cleaned_topics.append(tmp)
							cleaned_topics.append(tmp1)
						else:
							cleaned_topics.append(tmp+samecon)
						if con[i] in topics:
							topics.remove(con[i])
						if con[j] in topics:
							topics.remove(con[j])
		topics += cleaned_topics
		return topics

	def extract_topic_terms(self, T):
		"""Extract terms that define topics in the documents according to the T matrix obtained by SVD."""
		topics = []
		for row in range(T.T.shape[0]):
			sort =  numpy.argsort(T.T[row])
			tmp_con = []
			for x in range(len(sort)-10, len(sort)):
				if Document.vocabulary.get_word_by_index(sort[x]) not in tmp_con: 
					tmp_con.append(Document.vocabulary.get_word_by_index(sort[x]))
				
			for x in range(10):
				if Document.vocabulary.get_word_by_index(sort[x]) not in tmp_con: 
					tmp_con.append(Document.vocabulary.get_word_by_index(sort[x]))
			topics.append(tmp_con)
		return topics

	def process_documents(self):
		"""Build a term-document matrix and perform SVD on the matrix. The left matrix (T matrix) is used to extract topics after reduction of dimension to 4. Topics are then passed on to be cleaned. Terms that define a topic are given a higher weight in the documents that contain the words. """
		m = [ (len(self.documents))*[0] for i in range(Document.vocabulary.len()) ]
		matrix = numpy.ndarray(shape=(Document.vocabulary.len(), len(self.documents)), dtype=float)
		k = 4
		for i in range(len(self.documents)):
			ls = self.documents[i].bag_of_words.get_bag_as_list()
			for x in range(len(ls)):
				matrix[x][i] = ls[x]
		for doc in range(len(self.documents)):
			self.documents[doc].set_list_rep(matrix.T[doc])

		T,s,D = linalg.svd(matrix)
		T_original = T.copy()
		T.resize((len(T), k))
		dirty_topics = self.extract_topic_terms(T)
		self.topics = self.clean_topics(dirty_topics, T_original)

		for topic in self.topics:
			for term in topic:
				for d in self.documents:
					d.bag_of_words.add_importance_to_word(term)
		
		for doc in range(len(self.documents)):
			self.documents[doc].set_list_rep(self.documents[doc].bag_of_words.get_tf_idf())
		self.cluster_documents()

	def cluster_documents(self):
		"""Perform hierarchical clustering on the pre processed documents. """
		init_level = []
		for doc in self.documents:
			init_level.append(Cluster([doc], self.distance))
		self.clusters.append(init_level)

		iteration = len(self.documents)
		step = 1
		while len(self.clusters[len(self.clusters)-1]) > 1 and iteration > self.number_of_iterations:
			next_level = self.clusters[len(self.clusters)-1]
			merge_clusters = self.average_group_linkage()
			members = []
			for cluster in merge_clusters:
				members += cluster.content
				next_level.remove(cluster)
			next_level.append(Cluster(members, self.distance))
			self.clusters.append(next_level)
			self.print_cluster_step(next_level, iteration)
			iteration -= 1
			step += 1

	def print_cluster_step(self, level, step):
		"""Print clusters created in one iteration."""
		print "======================================================="
		print "Iteration: %s   Number of clusters:  %s"  % (step, len(self.clusters[len(self.clusters)-1]))
		clnum = 1
		for new in level:
			print "CLUSTER %s \n" % (clnum)
			new.print_members()
			print 
			clnum+=1

	def print_all_topics(self):
		"""Print all topics and terms defining it."""
		all_topics = ""
		i = 1
		for c in self.topics:
			stre = ""
			for x in c:
				stre+= ', '.join(Document.vocabulary.get_stem_word_mapping(Document.vocabulary.get_word_index(x))) + " | "

			all_topics += "Topic %s defined by terms: \n %s \n" % (i, stre)
			i += 1
		print all_topics

	def single_linkage(self):
		clos1,clos2 = None, None
		min_dist = -2
		for cl in self.clusters[len(self.clusters)-1]:
			for cl1 in self.clusters[len(self.clusters)-1]:
				if cl is not cl1:
					dist = -2
					for m in cl.content:
						for m1 in cl1.content:
							cos = self.distance.get_distance(m, m1)
							if (cos > dist):
								dist = cos
					if dist > min_dist:
						clos1 = cl
						clos2 = cl1
						min_dist = dist
		return [clos1, clos2]

	def complete_linkage(self):
		clos1,clos2 = None, None
		min_dist = -3333
		for cl in self.clusters[len(self.clusters)-1]:
			for cl1 in self.clusters[len(self.clusters)-1]:
				if cl is not cl1:
					dist = 200000
					for m in cl.content:
						for m1 in cl1.content:
							cos = self.distance.get_distance(m, m1)
							if (cos < dist):
								dist = cos
					if dist > min_dist:
						clos1 = cl
						clos2 = cl1
						min_dist = dist
		return [clos1, clos2]

	def average_linkage(self):
		clos1,clos2 = None, None
		min_dist = -3333
		for cl in self.clusters[len(self.clusters)-1]:
			for cl1 in self.clusters[len(self.clusters)-1]:
				if cl is not cl1:
					dist = 200000
					su = 0.0
					for m in cl.content:
						for m1 in cl1.content:
							cos = self.distance.get_distance(m, m1)
							su += cos
					div = 1.0/(len(self.content) * len(other.content))
					dist = div*su
					if dist > min_dist:
						clos1 = cl
						clos2 = cl1
						min_dist = dist
		return [clos1, clos2]

	def average_group_linkage(self):
		clos1,clos2 = None, None
		min_dist = -3333
		for cl in self.clusters[len(self.clusters)-1]:
			for cl1 in self.clusters[len(self.clusters)-1]:
				if cl is not cl1:
					dist = 200000
					su = 0.0
					content_both = []
					content_both += cl.content + cl1.content
					for m in content_both:
						for m1 in content_both:
							cos = self.distance.get_distance(m, m1)
							su += cos
					div = 1.0/(len(content_both)*(len(content_both)-1))
					dist = div*su

					if dist > min_dist:
						clos1 = cl
						clos2 = cl1
						min_dist = dist
		return [clos1, clos2]



class Cluster(object):
	"""Representation of a cluster contained in a HierarchicalClusterer."""
	def __init__(self, member, distance):
		super(Cluster, self).__init__()
		self.centroid = member[0]
		self.content = member
		self.distance = distance				

	def print_members(self):
		topics = ""
		for x in self.content:
			print x.title
			topics += ' | '.join(x.bag_of_words.topic_terms)
		print "\n Topic terms contained in this cluster: \n"
		print topics

		

		



		
		
		
				