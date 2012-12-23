#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
from httpclient import HttpClient
from htmlparser import between
from moviexml import *

url = 'http://www.movie2k.to/tvshows-1417991-Doctor-Who.html'
#sys.argv[1])

client = HttpClient()
client.GET(url)

if 'movie2k.to' in url:
	xml = MovieXML()
	url = between( between(client.Page, 'Watch movie', 'IMDB Rating'), '<a target="_blank" href="', '"' )
	series = between(client.Page, 'style="color:#000000;">', '<').strip().replace('\n', ' ')
	season = between(client.Page, '>, Season ', ',').strip()
	episode = between(client.Page, 'Episode ', '<').strip()

	movie = Movie(series=series, season=season, episode=episode)
	movie.append( Source(type='stream', url=url) )
	xml.append(movie)
	print str(xml)

