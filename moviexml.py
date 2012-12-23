#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#class page:

def indent(s):
	result = ''
	for line in s.split('\n'):
		result += '\t'+line+'\n'
	return result

class Source:
	def __init__(self, type=None, audio=None, subtitles=None, url=None):
		self.type = type
		self.audio = audio
		self.subtitles = subtitles
		self.url = url
		
	def __str__(self):
		xml = '<source'
		attr = {	'type':		self.type,
				'audio':		self.audio,
				'subtitles':	self.subtitles
			}
		for a in attr.keys():
			if attr[a] != None:
				xml += ' '+a+'="'+attr[a]+'"'
		xml += '>'+self.url+'</source>'
		return xml

class Episode:
	def __init__(self, id=None, title=None):
		self.id = id
		self.title = title
		self.children = []

	def append(self, child):
		self.children.append(child)

	def getSource(self, url):
		episode = None

		for child in self.children:
			if type(child) == Season:
				if child.url == url:
					source = child
					continue

		# not found: create
		if source is None:
			source = Source(url=url)
			self.children.append(source)
		return source

	def __str__(self):
		xml = '<episode'
		attr = {	'id':		self.id,
				'title':		self.title
			}
		for a in attr.keys():
			if attr[a] != None:
				xml += ' '+a+'="'+attr[a]+'"'
		xml += '>\n'
		for child in self.children:
			xml += indent(str(child))
		xml += '</episode>'
		return xml

class Season:
	def __init__(self, id=None):
		self.id = id
		self.children = []

	def append(self, child):
		self.children.append(child)

	def getEpisode(self, id):
		episode = None

		# find a child, that is a Series with the given title
		for child in self.children:
			if type(child) == Season:
				if child.id == id:
					episode = child
					continue

		# not found: create
		if episode is None:
			episode = Episode(id=id)
			self.children.append(episode)
		return episode

	def __str__(self):
		xml = '<season'
		attr = {	'id':		self.id	}
		for a in attr.keys():
			if attr[a] != None:
				xml += ' '+a+'="'+attr[a]+'"'
		xml += '>\n'
		for child in self.children:
			xml += indent(str(child))
		xml += '</season>'
		return xml

class Series:
	def __init__(self, title=None):
		self.title = title
		self.children = []

	def append(self, child):
		self.children.append(child)

	def getSeason(self, id):
		season = None

		# find a child, that is a Series with the given title
		for child in self.children:
			if type(child) == Season:
				if child.id == id:
					season = child
					continue

		# not found: create
		if season is None:
			season = Season(id=id)
			self.children.append(season)
		return season
		
	def __str__(self):
		xml = '<series'
		attr = {	'title':		self.title	}
		for a in attr.keys():
			if attr[a] != None:
				xml += ' '+a+'="'+attr[a]+'"'
		xml += '>\n'
		for child in self.children:
			xml += indent(str(child))
		xml += '</series>'
		return xml

class MovieXML:
	def __init__(self, debug=False):
		self.children = []

	def append(self, child):
		self.children.append(child)

	def getSeries(self, title):
		series = None

		# find a child, that is a Series with the given title
		for child in self.children:
			if type(child) == Series:
				if child.title == title:
					series = child
					continue

		# not found: create
		if series is None:
			series = Series(title=title)
			self.children.append(series)
		return series

	def __str__(self):
		xml = '<xml>\n'
		for child in self.children:
			xml += indent(str(child))
		xml += '</xml>'
		return xml

	def write(self, filename='movie.xml'):
		open(filename, 'w').write( str(self) )
