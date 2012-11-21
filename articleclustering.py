import json, distances, subprocess, os, time, signal, sys
from documentrep import Document
from clustering import Clusterer


def main():
	
	#start Stanford NER
	p = subprocess.Popen("java -mx1000m -cp stanford-ner/stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz -port 1239", shell=True)
	#wait ten sec to make sure NER is up and running
	time.sleep(10)

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
	print "Clustering finished ======================================================= \n"
	clus.print_all_topics()

	#kill NER
	os.kill(p.pid+1, 9)


if __name__ == '__main__':
	main()

