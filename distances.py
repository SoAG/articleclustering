from documentrep import Document
import math

registered_distances = []

def register_distance(dist_name):
	"""Register a specific distance."""
	register_distance.append(dist_name)

def register_all_distances():
	"""Register all distances that implement Distance()"""
	subs = Distance.__subclasses__()
	for sub in subs:
		registered_distances.append(sub.__name__) 
	print registered_distances

def get_distance(dist_name):
	"""Return instance of a specific distance."""
	if dist_name in registered_distances:
		return globals()[dist_name]()
	else:
		print "Distance not available. available distances are: %s" % (registered_distances)
	# print globals()



class Distance(object):
	"""Abstract class to define a distance. """
	def __init__(self):
		super(Distance, self).__init__()

	def get_distance(self, this, other):
		"""Get the distance between objects this and other."""
		raise NotImplementedError("Distance has not been implemented!")


class Euclidean(Distance):
	"""Euclidean distance"""
	def __init__(self):
		super(Euclidean, self).__init__()
		
	def get_distance(self, this, other):
		l1 = this.list_rep
		top = 0
		l2 = other.list_rep
		for x in xrange(0,len(l1)):
			top += (l1[x] - l2[x]) * (l1[x] - l2[x])
		return math.sqrt(top)

class Cosine(Distance):
	"""Cosine distance"""
	def __init__(self):
		super(Cosine, self).__init__()
		

	def get_distance(self, this, other):
		top = 0.0
		bl = 0.0
		br = 0.0
		l1 = this.list_rep
		l2 = other.list_rep
		for x in xrange(0,len(l1)):
			top += l1[x] * l2[x]
			bl += l1[x] * l1[x]
			br += l2[x] * l2[x]
		bl = math.sqrt(bl)
		br = math.sqrt(br)
		return top/(bl*br)
