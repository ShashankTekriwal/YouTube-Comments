from gdata.youtube import service
import gdata.youtube
import urlparse
import sys
import nltk
import re
import enchant
import os
import pickle
import requests
import json
import pprint

#########################GATHERING###########################

client = service.YouTubeService()
client.developer_key = 'AIzaSyCUNwYTPZzt3HsTmSq3eZElPnm6sgpjzm4'
videoID =['TRrL5j3MIvo']
searchWords=[]

def entryDetails(entry):
	vid_id = urlparse.parse_qs(urlparse.urlparse(entry.media.player.url).query)["v"][0]
	videoID.append(vid_id)

def VideoFeed(feed):
	for entry in feed.entry:
		entryDetails(entry)

def Search(search_terms):
	query = service.YouTubeVideoQuery()
	query.vq = search_terms
	query.orderBy = 'viewCount'
	query.racy = 'include'
	query.max_results = 5
	try:
		feed = client.YouTubeQuery(query)
	except:
		print "Unexpected error:", sys.exc_info()[0]
		print "Couldnt gather feeds for key "+ search_terms
		return
	VideoFeed(feed)

def comments_generator(client,url):
	comment_feed = client.GetYouTubeVideoCommentFeed(uri = url)
	try:
		while comment_feed is not None:
			for comment in comment_feed.entry:
				yield comment
			next_link = comment_feed.GetNextLink()
			if next_link is None:
				comment_feed = None
			else:
				comment_feed = client.GetYouTubeVideoCommentFeed(next_link.href)
	except :
		print "Unexpected error:", sys.exc_info()[0]
		print "Inside generator"
		return

# text_file = open("key_words.txt","r")
# searchWords = text_file.read().split('\n')
# for keys in searchWords:
# 	Search(keys)
# print videoID
key = raw_input("Enter search term: ")
Search(key)

for video in videoID:
	file_name = 'comments/'+video + '.txt';
	comment_feed_url = "http://gdata.youtube.com/feeds/api/videos/%s/comments?max-results=50&orderby=published"
	url = comment_feed_url % video
	f = open(file_name,'w')
	print 'Gathering comments for video ' + video
	count = 1
	try:
		for comment in comments_generator(client,url):
			text = comment.content.text
			if text is not None:
				text = " ".join(text.split("\n"))
			#author_name = comment.author[0].name.text
			f.write("{}".format(text)+'\n')
			print count
			count = count + 1
	except:
		print "Unexpected error:", sys.exc_info()[0]
		print "while calling generator"
		continue

#######################################stats################################

url = "https://www.googleapis.com/youtube/v3/videos?id=%s&part=statistics&key=AIzaSyCUNwYTPZzt3HsTmSq3eZElPnm6sgpjzm4"
url = url % ",".join(videoID)
data = requests.get(url)
data = data.json()
stats={}
for item in data['items']:
	print "Gathering statistics for video\t"+item['id']
	temp = {}
	temp['viewCount'] = item['statistics']['viewCount']
	temp['commentCount'] = item['statistics']['commentCount']
	temp['likeCount'] = item['statistics']['likeCount']
	temp['dislikeCount'] = item['statistics']['dislikeCount']
	stats[item['id']] = temp

####################################PRE#####################################
p = open('clfNB.pickle','rb')
clf = pickle.load(p)
p.close()
p = open('vectorizer.pickle' , 'rb')
vectorizer = pickle.load(p)
p.close()
d = enchant.Dict('en-US')

for video in videoID:
	print "Preprocessing comments for video\t"+video
	positive=0
	negative=0
	neutral=0
	f = open('comments/'+video+'.txt','r')
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
		new_sent = new_sent.lower()
		if (new_sent != "") and (new_sent != "None"):
			new_lines.append(new_sent)
	print "Classifying comments for video\t"+video
	data = vectorizer.transform(new_lines)
	result = clf.predict(data)
	for var in result:
		if var == '1':
			positive=positive+1
		elif var == '-1':
			negative=negative+1
		else:
			neutral=neutral+1
	stats[video]['posCommentCount'] = positive
	stats[video]['negCommentCount'] = negative
	stats[video]['neuCommentCount'] = neutral
	print "Result generated for video\t"+video

#####################################
pprint.pprint(stats)

#################################rate

ratings={}
for video_id in stats:

      if(stats[video_id]['negCommentCount']==0 and stats[video_id]['posCommentCount']==0 and stats[video_id]['likeCount']==0 and stats[video_id]['dislikeCount']==0):
            print 'Downloading comments for video_ID\t',video_id,'\tis restricted'
            ratings[video_id]=(float(int(stats[video_id]['likeCount']))/(int(stats[video_id]['viewCount'])+int(stats[video_id]['likeCount'])+int(stats[video_id]['dislikeCount'])))*6

      elif(stats[video_id]['viewCount']>=0 and stats[video_id]['viewCount']<=10000):
            ratings[video_id]=(float(int(stats[video_id]['likeCount'])))/(int(stats[video_id]['likeCount'])+int(stats[video_id]['dislikeCount']))*4 + (float(int(stats[video_id]['posCommentCount'])))/(int(stats[video_id]['negCommentCount'])+int(stats[video_id]['posCommentCount']))*6
      elif(stats[video_id]['viewCount']>10000 and stats[video_id]['viewCount']<=50000):
      		ratings[video_id]=(float(int(stats[video_id]['likeCount'])))/(int(stats[video_id]['likeCount'])+int(stats[video_id]['dislikeCount']))*5 + (float(int(stats[video_id]['posCommentCount'])))/(int(stats[video_id]['negCommentCount'])+int(stats[video_id]['posCommentCount']))*5
      elif(stats[video_id]['viewCount']>50000):
      		ratings[video_id]=(float(int(stats[video_id]['likeCount'])))/(int(stats[video_id]['likeCount'])+int(stats[video_id]['dislikeCount']))*6 + (float(int(stats[video_id]['posCommentCount'])))/(int(stats[video_id]['negCommentCount'])+int(stats[video_id]['posCommentCount']))*4

for video_id in ratings:
	print video_id,'\t',ratings[video_id]

ratings=sorted(ratings)
i=1

print 'Video ID','\t','Rank'

for video_id in ratings:
	print video_id,'\t',i
	i=i+1

