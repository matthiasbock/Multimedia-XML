#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
from httpclient import HttpClient
from htmlparser import between
from moviexml import *

try:
	url = sys.argv[1]
except:
	url = 'http://www.movie2k.to/Torchwood-watch-tvshow-627612.html'


def getTitle(page):
	return between(page, 'style="color:#000000;">', '<').strip().replace('\n', ' ')

def absoluteURL(pageURL):
	if pageURL[:4] != 'http':
		pageURL = 'http://www.movie2k.to/'+pageURL
	return pageURL

def addSource(_episode, url, audio=None, subtitles=None):
	url = url.replace('http://www.putlocker.com/embed/', 'http://www.putlocker.com/file/')
	_source= _episode.getSource(url)
	_source.type = 'stream'
	_source.audio = audio
	_source.subtitles = subtitles

def extractSource(page):
	url = between( between(page, 'Watch movie', 'IMDB Rating'), '<a target="_blank" href="', '"' )
	if url == '':
		url = between(page, '<div id="emptydiv"><iframe src="', '"')
	return url

def addAllSources(_episode, pageURL, audio=None, subtitles=None):
#	global client
#	menu = between(client.Page, '<tr id="', '<script>', include_before=True)
#	print menu
	
#	tr = between(menu, '<tr id="', '</tr>')
#	k = 0
#	while tr != '':
#		pageURL2 = absoluteURL( between(tr, '<a href="', '"') )
	pageURL2 = pageURL
	addSource(_episode, pageURL2, audio=audio, subtitles=subtitles)
	print '\tresolving '+pageURL2+' ->',
#		if pageURL2 != pageURL:
	client.GET(pageURL2)
	url = extractSource(client.Page)
	print url
	addSource(_episode, url, audio=audio, subtitles=subtitles)
#		k += 1
#		print str(k)
#		tr = between(menu, '<tr id="', '</tr>', skip=k)

def updateEpisodePageList(xml, page, audio=None, subtitles=None):
	seasons = []
	series = getTitle(page)
	_series = xml.getSeries(series)

	allSeasons_allEpisodes = between(page, '<FORM name="seasonform">', '</tr>')
	allSeasons = between(allSeasons_allEpisodes, '<SELECT name="season"', '</SELECT>')

	for i in range(4):
		season = between(allSeasons, '<OPTION value="', '"', skip=i)
		seasons.append(season.strip())

	j = 0
	for season in seasons:
		_season = _series.getSeason(season)
		allEpisodes = between(allSeasons_allEpisodes, '<FORM name="episodeform'+season+'">', '</FORM>', skip=j)
		j += 1
		#print allEpisodes
		i = 0
		episode = between(allEpisodes, '>Episode ', '</OPTION')
		while episode != '':
			#print 'Season '+season+', Episode '+episode
			pageURL = between(allEpisodes, '<OPTION value="', '"', skip=i)
			if pageURL != '':
				_episode = _season.getEpisode(episode)
				xml = addAllSources(_episode, absoluteURL(pageURL), audio=audio, subtitles=subtitles)
			i += 1
			episode = between(allEpisodes, '>Episode ', '</OPTION', skip=i)


 
xml = MovieXML()
client = HttpClient()

print 'GET '+url+' ...'
client.GET(url)
if 'us_flag_small.png' in str(client.Page):
	audio = 'en'
updateEpisodePageList(xml, client.Page, audio=audio, subtitles='-')

print str(xml)
