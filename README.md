#Article Clustering


##Approach

The documents are read from the json file and pre-processed. The pre-processing steps involve:
-	named entity recognition using the Stanford Named Entity Recognizer (NER) 	http://nlp.stanford.edu/software/CRF-NER.shtml.
	recognized named entities are removed from the text before any other pre-processing steps are executed.
-	stopword removal
-	stemming the words using a PorterStemmer (nltk - http://nltk.org/)

After the original article content has been pre-processed a BagOfWords is created for each document. The bag contains the frequencies of the words occurring in a document. Furthermore a bag of words is kept for the whole document collection. Stemmed words are put into the bag but also the original words are kept and mapped to the stem in order to easily retrieve them. The bag of words also contains the TF-IDF vector. 

After the articles have been read and are represented by a bag of words a Term- Document matrix is build and a Singular Value Decomposition is performed on th TD matrix. SVD enables one to find hidden concepts in the document space. This is used to extract topics/terms that are meaningful to the documents. Therefore the left-singular value matrix (T) is used which represents the term space (correlation of terms). First the dimensionality of T is reduced to only 4 dimensions in the columns. This reduced matrix is used to find terms that define the documents, to achieve this each column is sorted and the first 10 and last 10 terms are chosen from each column and represent a topic. This first 10 (biggest values) represent the words that co-occur most often in the documents, whereas the last (smallest values) represent words that only occur in a few documents. In a next step the topics extracted this way are cleaned because it is possible that they overlap. Overlap two topics in some words heavily these are merged into one topic, but in order not to merge two different topics together the T matrix is again used to check if words co-occur and only merge if they do otherwise a new topic is created.

The documents containing the terms that define a topic are then weighted according to the topic, meaning that the terms are given a higher importance. Afterwards the TF IDF for each document is created and the documents are ready to be clustered.

Hierarchical Agglomerative Clustering is used to build a hierarchy of clusters. As a metric the cosine distance is chosen. To link clusters together different strategies have been implemented (single_linkage, complete_linkage, average_linkage, average_group_linkage) and tested. The clusters are printed out in the command line after each iteration of the clustering algorithm. The algorithm was chosen because first results showed that it worked quiet well.

##Improvements
Hierarchical Clustering might not be the optimal way to cluster documents and it builds a structure which is not necessarily needed. Other clustering algorithms like EM-clustering or a density-based approach (i.e. majorclust, DBSCAN/OPTICS) are probably better suited. Another disadvantage of hierarchical clustering is that the runtime for larger document collections is too long. 

Furthermore I had the idea to use a multi-view clustering approach. Multi-View learning uses different representations(i.e. named entities, normal bag of words) for one document. Then one can use these different representations to train two cluster algorithms and exchange knowledge about the found clusters by each clusterer. 

Also I noticed that the bag of words contain many words that are noise so further cleaning of the words is necessary to improve the results. 

Topic extraction can be further improved i.e. using wordnet to query the found terms and map them to real concepts or word classes that really describe the bigger scheme of a article. Also reducing the number of dimensions to 4 can be better chosen or different values could be tested and chose the value that gives the best results by scoring the results for each tested value.

At the moment the topics are not mapped to the clusters. This could be achieved by calculating the likelihood of documents in a cluster belonging to each topic. (Did not have time to implement that yet)

##Usage
All libraries used are included. The Stanford NER should be started automatically when executing the python file and is listening on port 8342. If the stanford NER should not start it can be started from the command line executing the command:
java -mx1000m -cp stanford-ner/stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz -port 8342
from the "articleclustering" directory.

The program itself is started by: 
python articleclustering.py 6

the 6 stands for number of iterations and has to be given, but can be chosen to see results for different times in the stages of the hierarchical clusterer.


##Results
Good results were obtained with 10-12 iterations. As can be seen there is still some cleaning to be done in the term vector as well as the topic vectors.


============================================================================
Topics  
============================================================================ 


Topic 1 defined by terms:  

 guests,guest | state,stated,states | relationship,relationships | president,presidents,presidency | visit,visited,visiting | mr | peoples,people | obama | world | quee | oecd | growth | increase,increases,increasing | economy | 1 | remai | s | public | 8 | rates |     

Topic 2 defined by terms:      

 coningsby | lincolnshire | spokesperso | understood | unfit | raf coningsby | stationed | patrol | 10 | alcohol | o | saying,say,says | uk | governments,government,governance |     

Topic 3 defined by terms:    

 public | order | law | privacy | lawyers,lawyer | court,courts | informatio | users,user | health | nhs | england | spending | services,service | cent |     

Topic 4 defined by terms:    

 seaso | oecd | ca | growth | governments,government,governance | look,looked,looking,looks | ash | airlines,airline | cancelled,cancellations,cancel | o | airports,airport | travel,travelling,travelled | edinburgh | volcano,volcanoes |     

Topic 5 defined by terms:    

 public | order | law | privacy | lawyers,lawyer | s | court,courts | informatio | users,user | year,years | england | bee | services,service | cent |     

============================================================================
Clusters
============================================================================

Iteration: 10   Number of clusters:  8    
CLUSTER 1    

Flights cancelled as ash cloud heads towards UK   
Ash Cloud Clears UK 'But Set To Return'   

Topic terms contained in this cluster:    

state | relationship | presid | visit | mr | obama | 1 | remai | s | 8 | o | say | uk | england | servic | ash | airlin | cancel | airport | travel | edinburgh | volcano | year | beemr | remai | s | o | uk | england | ash | airlin | cancel | airport | travel | edinburgh | volcano | bee   

CLUSTER 2    

The Queen toasts Barack Obama and special relationship with the US   
Barack Obama says he would repeat Pakistan raid    

Topic terms contained in this cluster:    

guest | state | relationship | presid | visit | mr | peopl | obama | world | quee | s | o | say | uk | england | ca | look | beestate | relationship | presid | visit | peopl | obama | world | quee | 1 | s | o | say | england | ca | edinburgh | bee     

CLUSTER 3       

Owen wants to stay with United    
Manchester United manager Sir Alex Ferguson would love to re-sign Cristiano Ronaldo, says Marcello Lippi    

Topic terms contained in this cluster:     

s | o | say | england | seaso | ca | look | year | beerelationship | remai | s | o | say | england | seaso | ca | year    

CLUSTER 4     

Obama gives message of support to the Queen at lavish state banquet    
NHS in England to suffer smaller cuts than rest of UK    

Topic terms contained in this cluster:    

guest | state | relationship | presid | visit | mr | peopl | obama | world | quee | s | o | govern | law | servic | ca | look | edinburgh | year | beestate | peopl | s | o | say | govern | order | health | nhs | england | spend | servic | cent | look | year | bee    

CLUSTER 5     

Footballer's Twitter disclosure order prompts online action   
BA pilot jailed for killing wife    

Topic terms contained in this cluster:     

state | mr | peopl | s | public | o | say | uk | govern | order | law | privaci | lawyer | court | informatio | user | servic | ca | beequee | s | o | say | lawyer | court | year     

CLUSTER 6     

Libya unrest: UK 'undecided' on sending helicopters     
Libya Typhoon pilots sent home after 'night out'    

Topic terms contained in this cluster:     

state | mr | s | o | say | uk | govern | ca | bees | coningsbi | lincolnshire | spokesperso | understood | unfit | raf coningsby | station | patrol | 10 | alcohol | uk | ca | bee    

CLUSTER 7     

Egyptian pyramids found by infra-red satellite images    
Swimwear – this season's rules    

Topic terms contained in this cluster:     

visit | peopl | world | 1 | s | o | say | ca | look | travel | year | beeguest | world | s | o | say | ca | look | year | bee    

CLUSTER 8      

David Cameron to resist French plan for internet regulation    
Gordon Ramsay's father in law 'fathered two children by a mistress'    
Economy grows feebly in Q1 as household spending drops    
Interest rates must be raised this year, OECD warns    

Topic terms contained in this cluster:    

guest | state | presid | peopl | world | growth | 1 | remai | s | public | o | say | govern | law | privaci | lawyer | court | ca | look | yearmr | s | public | o | say | law | privaci | court | informatio | ca | look | year | beeoecd | growth | economi | 1 | remai | s | public | 8 | rate | o | govern | spend | look | year | beeoecd | growth | increas | economi | 1 | remai | s | public | 8 | rate | o | uk | govern | order | england | spend | year    

Clustering finished ======================================================= 

