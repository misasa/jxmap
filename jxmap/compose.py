import sys
import os
import yaml
from optparse import OptionParser
#from jxmap import __version__ as VERSION
from jxmap._version import __version__ as VERSION
from jxmap import Jxmap

def compose():
	prog = "jxmap-compose"
	parser = OptionParser(usage='usage: %prog [options] MAPFILE1 MAPFILE2 ...', version='%%prog %s' % VERSION)

	options, args = parser.parse_args()
 	_opts = eval(str(options))

	if len(args) < 1:
		parser.error("incorrect number of arguments")

	map_path = os.path.abspath(args[0])

	for map_path in args:
		jxmap = Jxmap(map_path=map_path)
		con = jxmap.condition
		print con
