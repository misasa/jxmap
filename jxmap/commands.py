import sys
import os
import numpy
from cv2 import cv
from optparse import OptionParser
from jxmap import __version__ as VERSION

def get_x_separated_args(option, opt, value, parser):
	setattr(parser.values, option.dest, tuple([ int(arg) for arg in value.split('x') ]))

def _parse_options():
	parser = OptionParser(usage='usage: %prog [options] MAPFILE', version='%%prog %s' % VERSION)
	parser.add_option("-g", "--geometry", type="string", action='callback', callback=get_x_separated_args,
		help='Specify "X-STEP-NUMBERxY-STEP-NUMBER".', dest="step_numbers"
		)
	parser.add_option("-b", "--swap-byte", dest="swap_byte",
		action='store_true',
		help='Swap byte order.', default=False
		)
	parser.add_option("-e", "--offset", type="int",
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
	imgArray = imgArray.reshape((x_step_number, y_step_number)).copy()
	imgArray = numpy.rot90(imgArray, 3).copy()

	return imgArray

def _output_path(path, ext = '.tiff'):
	root, org_ext = os.path.splitext(path)
	dirname = os.path.dirname(path)
	file_name = os.path.basename(root) + ext
	file_path = os.path.join(dirname, file_name)
	return file_path

def _get_rpl_text(imgArray):
	height, width = imgArray.shape
	dtype = imgArray.dtype
	data_length = imgArray.itemsize
	data_type = 'unsigned'

	if data_length == 8:
		data_type = 'float'

	rpl = ""
	rpl += "key\tvalue\n"
	rpl += "width\t%d\n" % width
	rpl += "height\t%d\n" % height
	rpl += "depth\t%d\n" % 1
	rpl += "offset\t%d\n" % 0
	rpl += "data-length\t%d\n" % data_length
	rpl += "data-type\t%s\n" % data_type
	rpl += "byte-order\tlittle-endian\n"
	rpl += "record-by\timage\n"

	return rpl

def _output_rpl(path, imgArray):
	rpl = _get_rpl_text(imgArray)
	f = open(path, 'w')
	f.write(rpl)

def _output_image(extension = '.tiff'):
	options, args = _parse_options()
	map_path = args[0]
	step_numbers = options.step_numbers
	x_step_number = step_numbers[0]
	y_step_number = step_numbers[1]
	#print "file:%s x:%d y:%d" % (map_path, x_step_number, y_step_number)s
	default_ofile_path = _output_path(map_path, extension)
	_opts = eval(str(options))
	imgArray = _read_map(map_path, x_step_number, y_step_number, **_opts)

	if extension == '.raw':
		imgArray.tofile(default_ofile_path)
		default_rpl_path = _output_path(map_path, '.rpl')
		_output_rpl(default_rpl_path, imgArray)

	else:
		imgArray = imgArray/float(numpy.amax(imgArray)) * 255
		imgArray = imgArray.astype(numpy.uint8).copy()
		pimg2 = cv.fromarray(imgArray)
		cv.SaveImage(default_ofile_path, pimg2)
	
def map2tiff():
	_output_image('.tiff')

def map2jpeg():
	_output_image('.jpeg')

def map2raw():
	_output_image('.raw')

