#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from httpclient import HttpClient
from htmlparser import between
from moviexml import *

def completeURL(pageURL):
	if len(pageURL) >0 and pageURL[:4] != 'http':
		pageURL = 'http://www.movie2k.to/'+pageURL
	return pageURL

#
# a page from Movie2k.to
#
class Movie2kPage:
	#
	# load from URL or page as string
	#
	def __init__(self, url=None, page=None):
		if page is None:
			client = HttpClient()
			client.GET(url)
			self.page = str(client.Page)
			del client
		else:
			self.page = page
	
	#
	# return the title of the current page's video
	#
	def extractTitle(self):
		return between(self.page, 'style="color:#000000;">', '<').strip().replace('\n', ' ')

	#
	# return the URL of the current page's video URL
	#
	def extractVideoLink(self, page=None):
		if page is None:
			page = self.page
		url = between( between(page, 'question.png', 'IMDB Rating'), '<a target="_blank" href="', '"' )
		if url == '':
			url = between(page, '<div id="emptydiv"><iframe src="', '"')
		url = url.replace('.com/embed/', '.com/file/')

		# movie splitted into several video files
		if 'teil1_aktiv.png' in page:
			print 'part 2 ...'
			client = HttpClient()
			client.GET( between( between(page, 'teil1_aktiv.png', 'teil2_inaktiv.png'), '<a href="', '"') )
			url = [url, extractVideoLink(client.Page)]
			del client
		return url

	#
	# return a dictionary of the video hosters listed on the current page or a specified URL
	#
	def extractHosters(self, URL=None):
		global client
		if URL != None:
			client.GET(URL)
			self.page = str(client.Page)
		
		self.hosters = {}
		
		i = 0
		tr = between(self.page, '<tr id="tablemoviesindex2"', "</tr>")
		while tr != '':
			link = completeURL( between(tr, '<a href="', '"') )
			if link != '':
				m = Movie2kPage(link)
				link = m.extractVideoLink()
				del m
			name = between( between(tr, '<td ', '</td>', skip=1), ' &nbsp;', '</a>' )
			self.hosters[name] = link
			i += 1
			tr = between(self.page, '<tr id="tablemoviesindex2"', "</tr>", skip=i)
		
		return self.hosters
	
	#
	# is it a series or is it a movie ?
	#
	def isSeries(self):
		return False
	
	#
	# return an array of the available seasons
	#
	def extractSeasons(self):
		selectSeason = between(self.page, '<SELECT name="season"', '</SELECT>')
		i = 0
		self.seasons = []
		season = between(selectSeason, '<OPTION value="', '"')
		while season != '':
			self.seasons.append(season.strip())
			i += 1
			season = between(selectSeason, '<OPTION value="', '"', skip=i)
		return self.seasons

	#
	# return a dictionary of the available {episode number:URL} pairs for a specific season
	#
	def extractEpisodes(self, season):
		allEpisodes = between(self.page, '<FORM name="episodeform'+season+'">', '</FORM>')
		i = 0
		self.episodes = {}
		episode = between(allEpisodes, '>Episode ', '</OPTION')
		while episode != '':
			pageURL = between(allEpisodes, '<OPTION value="', '"', skip=i)
			i += 1
			if pageURL != '':
				self.episodes[episode] = completeURL(pageURL)
			episode = between(allEpisodes, '>Episode ', '</OPTION', skip=i)
		return self.episodes


#
# inputs:
#	movie2k.to series page, HTML document as string
#	audio language (optional)
#	subtitle language (optional)
# function:
#	for all seasons:
#		for all episodes:
#			extract all hoster links and add them to the xml
#
def makeEpisodeList(xml, page, audio=None, subtitles=None):

	page = str(page)

	movie2k = Movie2kPage(page=page)

	# try audio language and subtitle auto-detect
	if 'us_flag_small.png' in page:
		audio = 'en'
	elif 'us_ger_small.png' in page:
		audio = 'de'
	if not ('subtitled' in page or 'subtitles' in page or 'Untertitel' in page or 'untertitelt' in page):
		subtitles='-'

	series = movie2k.extractTitle()
	_series = xml.getSeries(series)

	for season in movie2k.extractSeasons():
		_season = _series.getSeason(season.zfill(2))
		for episode in movie2k.extractEpisodes(season).keys():
			number = episode
			URL = movie2k.episodes[episode]
			_episode = _season.getEpisode(episode.zfill(2))
			for hoster in movie2k.extractHosters(URL).keys():

				print 'S'+season.zfill(2)+'E'+episode.zfill(2)+' - '+hoster+': '+movie2k.hosters[hoster]

				_hoster = _episode.getHoster( movie2k.hosters[hoster] )
				_hoster.type = 'stream'
				_hoster.name = hoster
				_hoster.audio = audio
				_hoster.subtitles = subtitles

	return series

