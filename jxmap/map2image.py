import sys
import os
import numpy
import re
import yaml
#from cv2 import cv
import Image
from optparse import OptionParser
from jxmap import __version__ as VERSION
from jxmap import Jxmap

def map2image():
	options, args = _parse_options()
 	#_opts = eval(str(options))


	map_path = os.path.abspath(args[0])
	out_path = os.path.abspath(args[1])

	if options.condition_file:
		jxmap = Jxmap(map_path=map_path, cnd_path=options.condition_file)
	else:
		jxmap = Jxmap(map_path=map_path)

	con = jxmap.condition

	if con:
		info = jxmap.sem_info()
		f = open(_change_extension(out_path, ".txt"), 'w')
		f.write(info)
		f.close()

	if con and con.get('scan_mode'):
		options.scan_mode = con.get('scan_mode')

	if options.step_numbers == None:
		if con and con.get('x_step_number') and con.get('y_step_number'):
			options.step_numbers = (con['x_step_number'], con['y_step_number'])

	if options.step_numbers == None:
		raise RuntimeError, "could not get xy-step-numbers. specify geometry or condition-file"

	step_numbers = options.step_numbers
	x_step_number = step_numbers[0]
	y_step_number = step_numbers[1]

	root, extension = os.path.splitext(out_path)
	dirname = os.path.dirname(out_path)
	base_name = os.path.basename(root)

	_opts = eval(str(options))

	#jxmap.load_map(**_opts)
	#imgArray = jxmap.data
	imgArray = Jxmap.read_map(map_path, x_step_number, y_step_number, **_opts)


	if extension == '.raw':
		imgArray.tofile(out_path)
		default_rpl_path = _output_path(out_path, '.rpl')
		_output_rpl(default_rpl_path, imgArray)

	else:
		imgArray = imgArray/float(numpy.amax(imgArray)) * 255
		imgArray = imgArray.astype(numpy.uint8).copy()
		pilImg = Image.fromarray(imgArray)
		pilImg.save(out_path)

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

	if len(args) != 2:
		parser.error("incorrect number of arguments")

	return options, args

def _output_path(path, ext = '.tiff'):
	return _change_extension(path, ext)


def _output_rpl(path, imgArray):
	rpl = _get_rpl_text(imgArray)
	f = open(path, 'w')
	f.write(rpl)

def _get_rpl_text(imgArray):
	height, width = imgArray.shape
	dtype = imgArray.dtype
	data_length = imgArray.itemsize
	data_type = 'unsigned'

	if data_length == 8:
		data_type = 'float'

	rpl = '''key\tvalue
width\t%d
height\t%d
depth\t%d
offset\t%d
data-length\t%d
data-type\t%s
byte-order\tlittle-endian
record-by\timage
''' % (width, height, 1, 0, data_length, data_type)

	return rpl


def _change_extension(path, extension):
	root, org_ext = os.path.splitext(path)
	dirname = os.path.dirname(path)
	file_name = os.path.basename(root) + extension
	file_path = os.path.join(dirname, file_name)
	return file_path
