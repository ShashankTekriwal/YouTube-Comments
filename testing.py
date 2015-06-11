#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.naive_bayes import MultinomialNB
import pickle



p = open('clfNB.pickle','rb')
clf = pickle.load(p)
p.close()
# p = open('X_array.pickle','rb')
# X = pickle.load(p)
# p.close()
# clf.fit(X,Y)
# p = open('Y_array.pickle' , 'rb')
# Y = pickle.load(p)
p = open('vectorizer.pickle' , 'rb')
vectorizer = pickle.load(p)
p.close()


data = vectorizer.transform([("There was a mistake Wasnt supposed and not He confused the actual charge with the distance of the two charges You would get and not").decode('utf-8-sig'),"good","needs matter"])
result = clf.predict(data)
print result
