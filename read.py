#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
from moviexml import *
from movie2k import *

try:
	url = sys.argv[1]
except:
	url = 'http://www.movie2k.to/Torchwood-watch-tvshow-627612.html'

xml = MovieXML()
source = Movie2kPage(url=url)
title = source.extractTitle()
if source.isSeries:
	print str( makeEpisodeList(xml, source.page) )
else:
	print str( source.extractHosters() )
xml.write(title+'.xml')
print title+'.xml written.'
