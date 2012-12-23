#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#class page:

class Source:
	def __init__(self, type=None, audio=None, subtitles=None, url=None, indent=2*'\t'):
		self.type = type
		self.audio = audio
		self.subtitles = subtitles
		self.url = url
		self.indent = indent
		
	def __str__(self):
		xml = self.indent+'<source '
		xml += 'url="'+self.url+'" '
		xml += '/>\n'
		return xml

class Movie:
	def __init__(self, type=None, series=None, season=None, episode=None, title=None, indent=1*'\t'):
		self.type = type
		self.season = season
		self.episode = episode
		self.title = title
		self.indent = indent
		self.children = []

	def append(self, child):
		self.children.append(child)
	
	def __str__(self):
		xml = self.indent+'<movie '
		attr = {	'type': 		self.type,
				'season':		self.season,
				'episode':	self.episode,
				'title':		self.title
			}
		for a in attr.keys():
			if attr[a] != None:
				xml += a+'="'+attr[a]+'" '
		xml += '>\n'
		for child in self.children:
			xml += str(child)
		xml += self.indent+'</movie>\n'
		return xml

class MovieXML:
	def __init__(self, debug=False):
		self.children = []

	def append(self, child):
		self.children.append(child)

	def __str__(self):
		xml = '<xml>\n'
		for child in self.children:
			xml += str(child)
		xml += '</xml>'
		return xml

	def write(self, filename='movie.xml'):
		open(filename, 'w').write( str(self) )
