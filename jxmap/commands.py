import sys
import os
import numpy
from cv2 import cv
from optparse import OptionParser
from jxmap import __version__ as VERSION

def _parse_options():
	parser = OptionParser(usage='usage: %prog [options] MAPFILE \'widthxheight\'', version='%%prog %s' % VERSION)
	parser.add_option("-s", "--swap-byte", dest="swap_byte",
		action='store_true',
		help='Swap byte order.', default=False
		)
	parser.add_option("-o", "--offset", type="int",
		help='Specify offset in byte.', default=0
		)
	options, args = parser.parse_args()
	return options, args

def _dtype(bytes_per_data):
	#bytes_per_data = file_size / data_count
	bytes_per_data = int(bytes_per_data)
	if bytes_per_data == 2:
		return 'u2'
	elif bytes_per_data == 4:
		return 'u4'
	elif bytes_per_data == 8:
		return 'f8'
	else:
		raise RuntimeError, "could not determine dtype"


def _read_map(path, x_step_number, y_step_number, **options):
	file_size = os.path.getsize(path)
	f = open(path, 'rb') 
	buffer = f.read()
	data_count = x_step_number * y_step_number
	bytes_per_data = file_size / data_count

	offset = file_size - data_count * bytes_per_data
	if options.get('offset', False):
		offset = options.get('offset')

	dtype = _dtype(bytes_per_data)
	imgArray = numpy.frombuffer(buffer, dtype=dtype, count=data_count, offset=offset).copy()

	if options.get('swap_byte', False):
		imgArray.byteswap(True)
	imgArray = imgArray.reshape((y_step_number, x_step_number)).copy()
#	imgArray = numpy.transpose(imgArray).copy()
	return imgArray

def _output_path(path, ext = '.tiff'):
	root, org_ext = os.path.splitext(path)
	dirname = os.path.dirname(path)
	file_name = os.path.basename(root) + ext
	file_path = os.path.join(dirname, file_name)
	return file_path

def map2tiff():
	options, args = _parse_options()
	map_path = args[0]
	x_step_number = int(args[1])
	y_step_number = int(args[2])
	print "file:%s x:%d y:%d" % (map_path, x_step_number, y_step_number)
	_opts = eval(str(options))
	imgArray = _read_map(map_path, x_step_number, y_step_number, **_opts)
	pimg2 = cv.fromarray(imgArray)
	default_ofile_path = _output_path(map_path, '.tiff')
	print "%s writing..." % default_ofile_path
	cv.SaveImage(default_ofile_path, pimg2)

def map2jpeg():
	options, args = _parse_options()
	map_path = args[0]
	x_step_number = int(args[1])
	y_step_number = int(args[2])
	print "file:%s x:%d y:%d" % (map_path, x_step_number, y_step_number)
	_opts = eval(str(options))
	imgArray = _read_map(map_path, x_step_number, y_step_number, **_opts)
	pimg2 = cv.fromarray(imgArray)
	default_ofile_path = _output_path(map_path, '.jpeg')
	print "%s writing..." % default_ofile_path
	cv.SaveImage(default_ofile_path, pimg2)

def map2raw():
	options, args = _parse_options()
	map_path = args[0]
	x_step_number = int(args[1])
	y_step_number = int(args[2])
	print "file:%s x:%d y:%d" % (map_path, x_step_number, y_step_number)
	_opts = eval(str(options))
	imgArray = _read_map(map_path, x_step_number, y_step_number, **_opts)
	imgArray = numpy.transpose(imgArray).copy()
	height, width = imgArray.shape
	default_ofile_path = _output_path(map_path, '.raw')
	default_rpl_path = _output_path(map_path, '.rpl')
	print "%s writing..." % default_ofile_path
	print "%s writing..." % default_rpl_path
	imgArray.astype('uint16').tofile(default_ofile_path)
	rpl = open(default_rpl_path, 'w')
	rpl.write("key\tvalue\n")
	rpl.write("width\t%d\n" % height)
	rpl.write("height\t%d\n" % width)
	rpl.write("depth\t%d\n" % 1)
	rpl.write("offset\t%d\n" % 0)
	rpl.write("data-length\t%d\n" % 2)
	rpl.write("data-type\tunsigned\n")
	rpl.write("byte-order\tlittle-endian\n")
	rpl.write("record-by\timage\n")


