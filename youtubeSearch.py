import gdata.youtube
import gdata.youtube.service
yt_service = gdata.youtube.service.YouTubeService()
yt_service.developer_key = 'AIzaSyCUNwYTPZzt3HsTmSq3eZElPnm6sgpjzm4'
count = 0
def PrintEntryDetails(entry):
  print 'Video title: %s' % entry.media.title.text
  # print 'Video published on: %s ' % entry.published.text
  # print 'Video description: %s' % entry.media.description.text
  # print 'Video category: %s' % entry.media.category[0].text
  # print 'Video tags: %s' % entry.media.keywords.text
  # print 'Video watch page: %s' % entry.media.player.url
  # print 'Video flash player URL: %s' % entry.GetSwfUrl()
  # print 'Video duration: %s' % entry.media.duration.seconds
  ##print 'Video geo location: %s' % entry.geo.location()
  # print 'Video view count: %s' % entry.statistics.view_count
  print 'Video statistics %s' % entry.statistics
  print 'Video rating: %s' % entry.rating
  print 'Video media: %s' % entry.media

  ##print 'Video viewWatchCount count: %s' % entry.statistics.view_watch_count
  ##print 'Video suscriber count: %s' % entry.statistics.suscriber_count
  # print 'Video favourite count: %s' % entry.statistics.favorite_count
  # print 'Video last web access: %s' % entry.statistics.last_web_access
  # print 'Video rating: %s' % entry.rating.average
  print '.................................................................................................'
def PrintVideoFeed(feed):
	print len(feed.entry)
  	for entry in feed.entry:
  		PrintEntryDetails(entry)
def SearchAndPrint(search_terms):
  yt_service = gdata.youtube.service.YouTubeService()
  query = gdata.youtube.service.YouTubeVideoQuery()
  query.vq = search_terms
  query.orderby = 'viewCount'
  query.racy = 'include'
  query.max_results = 1
  feed = yt_service.YouTubeQuery(query)
  PrintVideoFeed(feed)
SearchAndPrint('android tutorials')