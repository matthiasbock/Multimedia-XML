#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#class page:

class Source:
	def __init__(self, type=None, audio=None, subtitles=None, url=None, indent=2):
		self.type = type
		self.audio = audio
		self.subtitles = subtitles
		self.url = url
		self.indent = indent
		
	def __str__(self):
		xml = self.indent*'\t'+'<source '
		xml = xml.strip()
		xml += '>\n'
		return xml

class Movie:
	def __init__(self, type=None, series=None, season=None, episode=None, title=None, indent=1):
		self.type = type
		self.season = season
		self.episode = episode
		self.title = title
		self.indent = indent
		self.children = []

	def append(self, child):
		self.children.append(child)
	
	def __str__(self):
		xml = self.indent*'\t'+'<movie '
		if self.type != None:
			xml += 'type="" '
		xml = xml.strip()
		xml += '>\n'
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
