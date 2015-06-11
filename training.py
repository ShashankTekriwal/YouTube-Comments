from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import os
import pickle


vectorizer = CountVectorizer(min_df = 0.0001 , ngram_range = (1,2) ,binary = True)
#f = open('refine.txt','r')
corpus = []
Y = []

def train():
	for txt in os.listdir('comments2'):
		f = open('comments_tagged/'+txt,'r')
		print "reading in file\t"+txt
		for line in f:
			part = line.split(';')
			corpus.append(part[0].encode('utf-8'))
			Y.append(part[1].split('\n')[0])
		f.close()
	X = vectorizer.fit_transform(corpus)
	return X

X = train()
# p = open('X_array.pickle' , 'wb')
# pickle.dump(X,p)
# p.close()
p = open('vectorizer.pickle' , 'wb')
pickle.dump(vectorizer,p)
p.close()
# p = open('Y_array.pickle' , 'wb')
# pickle.dump(Y , p)
# p.close()
#print 'X formed'
features = vectorizer.get_feature_names()
print 'features formed'
print len(features)
clf = MultinomialNB()
clf.fit(X,Y)
p = open ('clfNB.pickle','wb')
pickle.dump(clf,p)
p.close()
#print X.toarray()
#print vectorizer.vocabulary_
#print corpus
#------------------------test data------------