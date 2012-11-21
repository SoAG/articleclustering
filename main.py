import json, distances, subprocess, os, time, signal, sys
from documentrep import Document
from clustering import Clusterer


def main():
	
	p = subprocess.Popen("java -mx1000m -cp stanford-ner/stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz -port 1239", shell=True)
	time.sleep(5)
	# sts = os.waitpid(p.pid, 0)
	datafile = open('data/data.json', 'r')
	data = json.load(datafile)
	documents = []
	for article in data['articles']:
		document = Document(article)
		documents.append(document)

	distances.register_all_distances()
	d = distances.get_distance("Cosine")
	clus = Clusterer(documents, d, int(sys.argv[1]))
	clus.process_documents()
	clus.print_all_topics()
	print p.pid

	# print os.kill(p.pid+1, 9)


if __name__ == '__main__':
	main()

