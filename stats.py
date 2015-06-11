import requests , json , pprint
#data = requests.get("https://www.googleapis.com/youtube/v3/videos?chart=mostpopular&part=statistics,snippet&key=AIzaSyCUNwYTPZzt3HsTmSq3eZElPnm6sgpjzm4&orderby=viewcount")
#pprint.pprint(data.json())
url = "https://www.googleapis.com/youtube/v3/videos?id=%s&part=statistics&key=AIzaSyCUNwYTPZzt3HsTmSq3eZElPnm6sgpjzm4"
vid = ['KipSEcE6gGM','TaG9SDxwPBg']
string=""
for video in vid:
	string = string+video+","
string = ",".join(vid)
url=url%string
data=requests.get(url)
data = data.json()
stats = {}
#pprint.pprint(data['items'][0]['snippet']['description'])
for item in data['items']:
	counts = []
	counts.append(item['statistics']['viewCount'])
	counts.append(item['statistics']['likeCount'])
	counts.append(item['statistics']['dislikeCount'])
	counts.append(item['statistics']['commentCount'])
	stats[item['id']] = counts
#print stats
pprint.pprint(stats)
#print stats['7Ql1T41Jw5U'][0]
stats['hello'] = {'a':'b','c':0}
stats['hello']['d'] = 'l'
pprint.pprint(stats)