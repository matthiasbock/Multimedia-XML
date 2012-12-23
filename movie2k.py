#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#import sys
from httpclient import HttpClient
from htmlparser import between
from moviexml import *

def parseSinglePage(page, audio=None, subtitles=None):
	series = between(page, 'style="color:#000000;">', '<').strip().replace('\n', ' ')
	season = between(page, '>, Season ', ',').strip()
	episode = between(page, 'Episode ', '<').strip()

	url = between( between(page, 'Watch movie', 'IMDB Rating'), '<a target="_blank" href="', '"' )
	if url == '':
		url = between( page, '<div id="emptydiv"><iframe src="', '"')
	url = url.replace('http://www.putlocker.com/embed/', 'http://www.putlocker.com/file/')

	global xml
	_series = xml.getSeries(series)
	_season = _series.getSeason(season)
	_episode = _season.getEpisode(episode)
	_source= _episode.getSource(url)
	_source.type = 'stream'
	_source.audio = audio
	_source.subtitles = subtitles
 
xml = MovieXML()
client = HttpClient()

print 'GET ...'
client.GET('http://www.movie2k.to/tvshows-1417991-Doctor-Who.html')
parseSinglePage(client.Page, audio='en', subtitles='-')
print str(xml)

print 'GET ...'
client.GET('http://www.movie2k.to/Torchwood-watch-tvshow-627612.html')
parseSinglePage(client.Page, audio='en', subtitles='-')
print str(xml)
