#!/usr/bin/env python
import sys
import os
import numpy
from optparse import OptionParser
#sys.path.insert(0, os.path.dirname( os.path.abspath( __file__ ) ) + "/../lib")
#import mylib
from jxmap import __version__ as VERSION
from jxmap import load_rpl, load_raw

def u8raw():
	# parser = OptionParser("usage: %prog [options] rawfile ...")
	parser = OptionParser("""usage: %prog [options] rawfile0 [rawfile1 ...]

SYNOPSIS AND USAGE
  python %prog [options] rawfile0 [rawfile1 ...]

DESCRIPTION
  Reduce size of mapfile by getting rid of lighter bits.  This
  program converts raw mapfile (rawfile) produced by JXA-8530F
  to unsinged 8-bit integer (char).  Raw mapfile can be float
  32-bit or unsigned 16-bit integer.  This is useful when a
  map is too large and consumes lots of memory.

EXAMPLE
  DOS> ls
  Al.raw  Al.rpl
  DOS> python u8raw.py Al.raw
  ...
  DOS> ls
  Al.raw  Al_u8.raw  Al_u8.rpl

SEE ALSO
  python phase_analysis.py
  http://dream.misasa.okayama-u.ac.jp
  http://www.nist.gov/lispix/

IMPLEMENTATION
  Orochi, version 9
  Copyright (C) 2014 Okayama University
  License GPLv3+: GNU GPL version 3 or later

HISTORY
  July 2, 2015: TK adds documentation
""")
	parser.add_option("-v", "--verbose",
	                  action="store_true", dest="verbose", default=False,
	                  help="make lots of noise")

	(options, args) = parser.parse_args()
	if len(args) < 1:
	    parser.error("incorrect number of arguments")

	imlist = []
	basenames = []
	for arg in args:
		root, ext = os.path.splitext(arg)
		basenames.append(os.path.basename(root))	
		imlist.append(arg)

	max_all = -10000
	for raw_path in imlist:
		root, ext = os.path.splitext(raw_path)
		dirname = os.path.dirname(raw_path)
		rpl_path = os.path.join(dirname, os.path.basename(root) + '.rpl')
		rpl = load_rpl(rpl_path)
		data = load_raw(raw_path, rpl)
		max_i = numpy.max(data)
		if max_i > max_all:
			max_all = max_i

	for raw_path in imlist:
		root, ext = os.path.splitext(raw_path)
		dirname = os.path.dirname(raw_path)
		basename = os.path.basename(root)
		rpl_path = os.path.join(dirname, basename + '.rpl')
		reduced_raw_path = os.path.join(dirname, basename + '_u8.raw')
		reduced_rpl_path = os.path.join(dirname, basename + '_u8.rpl')
		
		rpl = load_rpl(rpl_path)
		data = numpy.array(load_raw(raw_path, rpl), dtype=float)/float(max_all) * 255
		numpy.array(data).astype('int8').tofile(reduced_raw_path)
		
		reduced_rpl = open(reduced_rpl_path, 'w')
		reduced_rpl.write("key\tvalue\n")
		reduced_rpl.write("width\t%d\n" % int(rpl["width"]))
		reduced_rpl.write("height\t%d\n" % int(rpl["height"]))
		reduced_rpl.write("depth\t%d\n" % 1)
		reduced_rpl.write("offset\t%d\n" % 0)
		reduced_rpl.write("data-length\t%d\n" % 1)
		reduced_rpl.write("data-type\tunsigned\n")
		reduced_rpl.write("byte-order\tdont-care\n")
		reduced_rpl.write("record-by\timage\n")
		reduced_rpl.close()
		
