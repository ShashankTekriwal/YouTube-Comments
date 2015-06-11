from gdata.youtube import service
import gdata.youtube
import urlparse
import sys

client = service.YouTubeService()
client.developer_key = 'AIzaSyCUNwYTPZzt3HsTmSq3eZElPnm6sgpjzm4'
videoID =['rkvEM5Y3N60']
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

text_file = open("key_words.txt","r")
searchWords = text_file.read().split('\n')
for keys in searchWords:
	Search(keys)
print videoID

for video in videoID:
	file_name = 'comments/'+video + 'copy.txt';
	comment_feed_url = "http://gdata.youtube.com/feeds/api/videos/%s/comments?max-results=50&orderby=published"
	url = comment_feed_url % video
	f = open(file_name,'w')
	print 'gathering comments for video ' + video
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
