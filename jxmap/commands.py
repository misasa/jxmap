import sys
import os
import numpy
import re
#from cv2 import cv
import Image
from optparse import OptionParser
from jxmap import __version__ as VERSION

def get_x_separated_args(option, opt, value, parser):
	setattr(parser.values, option.dest, tuple([ int(arg) for arg in value.split('x') ]))

def _parse_options():
	prog = "jxmap-image"
	parser = OptionParser(usage='usage: %prog [options] MAPFILE IMAGEFILE', version='%%prog %s' % VERSION)
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
	parser.add_option("-c", "--condition-file", type="string",
		help='Specify condition file.'
		)

	options, args = parser.parse_args()
 	_opts = eval(str(options))

	if len(args) != 2:
		parser.error("incorrect number of arguments")

	map_path = os.path.abspath(args[0])
	out_path = os.path.abspath(args[1])


	con = _get_condition(map_path, **_opts)
	if options.step_numbers == None:
		if con and con['x_step_number'] and con['y_step_number']:
			options.step_numbers = (con['x_step_number'], con['y_step_number'])

	if options.step_numbers == None:
		raise RuntimeError, "could not get xy-step-numbers. specify geometry or condition-file"

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
	return _change_extension(path, ext)	

def _change_extension(path, extension):
	root, org_ext = os.path.splitext(path)
	dirname = os.path.dirname(path)
	file_name = os.path.basename(root) + extension
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

def _cnd_path(path):
	root, org_ext = os.path.splitext(path)
	dirname = os.path.dirname(path)
	base_name = os.path.basename(root)
	return os.path.join(dirname, base_name + '.cnd')

def _cnd_path_0(path):
	root, org_ext = os.path.splitext(path)
	dirname = os.path.dirname(path)
	base_name = os.path.basename(root)
	return os.path.join(dirname, '0.cnd')

def _parse_condition_feepma(buffer):
#	print buffer
	dic = {}
	m = re.search(r'\$XM_AP_SA_PIXELS%(\d+) (\d+) (\d+)', buffer)
	if m:
		dic['x_step_number'] = int(m.group(2))
		dic['y_step_number'] = int(m.group(3))

	return dic

def _parse_condition_jxa1(buffer):
	dic = {}
	m = re.search(r'(\d+)\s+X-axis Step Number \[1~1024\]', buffer)
	if m:
		dic['x_step_number'] = int(m.group(1))
	m = re.search(r'(\d+)\s+Y-axis Step Number \[1~1024\]', buffer)
	if m:
		dic['y_step_number'] = int(m.group(1))
	return dic

def _parse_condition(buffer):
	if re.match(r'\$', buffer):
		return _parse_condition_feepma(buffer)
	else:
		return _parse_condition_jxa1(buffer)

def _read_condition(path, **options):
	buffer = None
	if options.get('condition_file', False):
		cnd_path = os.path.abspath(options.get('condition_file'))
		if os.path.exists(cnd_path):
			buffer = open(cnd_path, 'r').read()
		else:
			raise RuntimeError, "could not find %s" % cnd_path
	else:
		cnd_path = _cnd_path(path)
		cnd_path_0 = _cnd_path_0(path)
		print cnd_path
		print cnd_path_0
		if os.path.exists(cnd_path):
			buffer = open(cnd_path, 'r').read()
		elif os.path.exists(cnd_path_0):
			buffer = open(cnd_path_0, 'r').read()
	return buffer

def _get_condition(path, **options):
	buffer = _read_condition(path, **options)
	if buffer:
		return _parse_condition(buffer)

def map2image():
	options, args = _parse_options()
	map_path = os.path.abspath(args[0])
	out_path = os.path.abspath(args[1])
	step_numbers = options.step_numbers
	x_step_number = step_numbers[0]
	y_step_number = step_numbers[1]
	#print "file:%s x:%d y:%d" % (map_path, x_step_number, y_step_number)s
	#default_ofile_path = _output_path(map_path, extension)

	root, extension = os.path.splitext(out_path)
	dirname = os.path.dirname(out_path)
	base_name = os.path.basename(root)

	if (not dirname == '') and (not os.path.exists(dirname)):
		os.makedirs(dirname)

	_opts = eval(str(options))
	imgArray = _read_map(map_path, x_step_number, y_step_number, **_opts)

	if extension == '.raw':
		imgArray.tofile(out_path)
		default_rpl_path = _output_path(out_path, '.rpl')
		_output_rpl(default_rpl_path, imgArray)

	else:
		imgArray = imgArray/float(numpy.amax(imgArray)) * 255
		imgArray = imgArray.astype(numpy.uint8).copy()
		pilImg = Image.fromarray(imgArray)
		pilImg.save(out_path)
		#pimg2 = cv.fromarray(imgArray)
		#cv.SaveImage(out_path, pimg2)

# def map2tiff():
# 	_output_image('.tiff')

# def map2jpeg():
# 	_output_image('.jpeg')

# def map2raw():
# 	_output_image('.raw')

