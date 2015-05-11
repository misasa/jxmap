import sys
import os
import yaml
from optparse import OptionParser
from jxmap import __version__ as VERSION
from jxmap import Jxmap

def map2info():
	prog = "jxmap-info"
	parser = OptionParser(usage='usage: %prog [options] MAPFILE', version='%%prog %s' % VERSION)
	parser.add_option("-c", "--condition-file", type="string",
		help='Specify condition file.'
		)

	options, args = parser.parse_args()
 	_opts = eval(str(options))

	if len(args) != 1:
		parser.error("incorrect number of arguments")

	map_path = os.path.abspath(args[0])

	if _opts.get('condition_file', False):
		jxmap = Jxmap(map_path=map_path, cnd_path=_opts.get('condition_file'))
	else:
		jxmap = Jxmap(map_path=map_path)

	con = jxmap.condition
	#con = _get_condition(map_path, **_opts)
	if con:
		print yaml.dump(con)
