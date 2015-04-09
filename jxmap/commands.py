import sys
from optparse import OptionParser
from jxmap import __version__ as VERSION

def _parse_options():
	parser = OptionParser(usage='usage: %prog [options]', version='%%prog %s' % VERSION)
	parser.add_option("-b", "--byte-order", dest="byte_order",
		help='Specify byte order (little-endian or big-endian).',
		metavar="BYTE_ORDER"
		)
	options, args = parser.parse_args()
	return options, args

def map2tiff():
	options, args = _parse_options()
	print "map2tiff..."
def map2jpeg():
	options, args = _parse_options()
	print "map2jpeg..."

def map2raw():
	options, args = _parse_options()
	print options
	print args