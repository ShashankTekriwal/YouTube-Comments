import nltk
import re
import enchant
import os


d = enchant.Dict('en-US')
pos = open("pos.txt").read().split()
neg = open("neg.txt").read().split()
#f = open('rkvEM5Y3N60copy.txt','r')

for txt in os.listdir('comments2/'):
	f = open('comments2/'+txt,'r')
	tokens=[]
	new_lines=[]
	for line in f:
		#line = ''.join(line)
		line = re.sub('[^A-Za-z0-9 ]+','',line)
		line = re.sub(r'(.)\1{2,}' , r'\1\1' , line )
		tokens.append(nltk.pos_tag(nltk.word_tokenize(line)))
	f.close()
	for t in tokens:
		#req_words=[]
		new_sent = ""
		for tt in t:
			det = tt[1]
			if (det=="RB" or det=="VBG" or det == "JJ" or det == "RBR" or det == "RBS"
			or det=="JJR"or det == "JJS" or det=="NNS" or det == "NN") and d.check(tt[0]) :
				new_sent = new_sent + tt[0] + " "
		new_sent = new_sent.strip()
		if (new_sent != "") and (new_sent != "None"):
			new_lines.append(new_sent)
	f = open("comments_tagged/"+txt,"w")
	for line in new_lines:
		#print line
		line = line.lower()
		words = line.split()
		#print words
		pol = 0
		for word in words:
			if word in pos:
				pol = pol + 1
			elif word in neg :
				pol = pol - 1
		if pol > 0 :
			f.write(line+';1\n')
		elif pol < 0 :
			f.write(line+';-1\n')
		else:
			f.write(line+';0\n')
	f.close()
#print len(new_lines)
