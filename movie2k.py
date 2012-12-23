#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#import sys
from httpclient import HttpClient
from htmlparser import between
from moviexml import *

def parseSinglePage(url):
	client = HttpClient()
	client.GET(url)

	url = between( between(client.Page, 'Watch movie', 'IMDB Rating'), '<a target="_blank" href="', '"' )
	series = between(client.Page, 'style="color:#000000;">', '<').strip().replace('\n', ' ')
	season = between(client.Page, '>, Season ', ',').strip()
	episode = between(client.Page, 'Episode ', '<').strip()

	global xml
	_series = xml.getSeries(series)
	_season = _series.getSeason(season)
	_episode = _season.getEpisode(episode)
	_source= _episode.getSource(url)
	_source.type = 'stream'
 
xml = MovieXML()
print 'GET ...'
parseSinglePage('http://www.movie2k.to/tvshows-1417991-Doctor-Who.html')
print str(xml)
print 'GET ...'
parseSinglePage('http://www.movie2k.to/tvshows-1454111-Torchwood.html')
print str(xml)
