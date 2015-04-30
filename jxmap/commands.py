import sys
import os
import numpy
import re
import yaml
#from cv2 import cv
import Image
from optparse import OptionParser
from jxmap import __version__ as VERSION

def map2image():
	options, args = _parse_options()

	map_path = os.path.abspath(args[0])
	out_path = os.path.abspath(args[1])
	step_numbers = options.step_numbers
	x_step_number = step_numbers[0]
	y_step_number = step_numbers[1]

	root, extension = os.path.splitext(out_path)
	dirname = os.path.dirname(out_path)
	base_name = os.path.basename(root)

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

	con = _get_condition(map_path, **_opts)
	if con:
		print yaml.dump(con)

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

	if con:
		info = _get_info_text(con)
		f = open(_change_extension(out_path, ".txt"), 'w')
		f.write(info)
		f.close()
		f = open(_change_extension(out_path, ".info"), 'w')
		f.write(yaml.dump(con))
		f.close()

	if con and con.get('scan_mode'):
		options.scan_mode = con.get('scan_mode')

	if options.step_numbers == None:
		if con and con.get('x_step_number') and con.get('y_step_number'):
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
	#print "%s %dx%d %d %d %d" % (path, x_step_number, y_step_number, file_size, offset, bytes_per_data)
	dtype = _dtype(bytes_per_data)

	imgArray = numpy.frombuffer(buffer, dtype=dtype, count=data_count, offset=offset).copy()

	if options.get('swap_byte', False):
		imgArray.byteswap(True)

	if options.get('scan_mode', 'S') == 'B':
		imgArray = imgArray.reshape((y_step_number, x_step_number)).copy()
	else:
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

def _get_info_text(con):
	# title_text = con.get('comment', 'map')
	# if con.get('signal'):
	# 	title_text += " " + con.get('signal')
	# title = "$CM_TITLE %s" % (title_text)
	# if con.get('magnification'):
	# 	mag = "$CM_MAG %.0f" % (con['magnification'])
#	size = "$CM_FULL_SIZE %d %d" % (con['x_step_number'],con['y_step_number'])
#	stage_position = "$CM_STAGE_POS %s %s %s 0 0 0" % (con['x_stage_position'], con['y_stage_position'], con['z_stage_position'])

	info = "$CM_TITLE %s %s\n" % (con.get('comment', 'map'), con.get('signal', 'signal'))
	info += "$CM_MAG %.0f\n" % con.get('magnification', 1)
	info += "$CM_FULL_SIZE %d %d\n" % (con.get('x_step_number', 0), con.get('y_step_number', 0))
	info += "$CM_STAGE_POS %s %s %s 0 0 0\n" % (con.get('x_stage_position', '0'), con.get('y_stage_position', '0'), con.get('z_stage_position', '0'))
	info += "$$SM_SCAN_ROTATION 0.00\n"
	return info

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

def _magnification(width_in_um):
	return 120000/float(width_in_um)

def _parse_condition_feepma(buffer):
	#print buffer
	dic = {}
	m = re.search(r'SA_PIXELS%(\d+) (\d+) (\d+)', buffer)
	if m:
		x_step_number = int(m.group(2))
		dic['x_step_number'] = x_step_number
		dic['y_step_number'] = int(m.group(3))
		m = re.search(r'\$XM_AP_SA_PIXEL_SIZE%(\d+) (\S+) (\S+) (\S+)', buffer)
		if m:
			x_step_size = float(m.group(2))
			dic['x_step_size'] = x_step_size
			dic['y_step_size'] = float(m.group(3))

			width_in_um = x_step_size * x_step_number
			dic['magnification'] = _magnification(width_in_um)

	m = re.search(r'\$XM_AP_SA_STAGE_POS%(\d+)_0 (\S+) (\S+) (\S+)', buffer)
	if m:
		dic['scan_mode'] = 'S'
		dic['x_stage_position'] = m.group(2)
		dic['y_stage_position'] = m.group(3)
		dic['z_stage_position'] = m.group(4)

	m = re.search(r'\$XM_AP_BSA_STAGE_POS%(\d+) (\S+) (\S+) (\S+)', buffer)
	if m:
		dic['scan_mode'] = 'B'
		dic['x_stage_position'] = m.group(2)
		dic['y_stage_position'] = m.group(3)
		dic['z_stage_position'] = m.group(4)


	m = re.search(r'\$XM_AP_COMMENT%(\d+) (\S+)', buffer)
	if m:
		dic['comment'] = m.group(2)

	m = re.search(r'\$XM_ELEM_WDS_COND_NAME%(\d+) (\S+)', buffer)
	if m:
		dic['signal'] = m.group(2)
		vals = m.group(2).split('_')
		dic['element_name'] = vals[0]
		dic['channel_name'] = vals[1]
		dic['crystal_name'] = vals[2]
		dic['x_ray_name'] = vals[3]
	m = re.search(r'\$XM_ELEM_IMS_SIGNAL_TYPE%(\d+) (\S+)', buffer)
	if m:
		dic['signal'] = m.group(2)

	return dic

def _parse_condition_jxa1(buffer):
	dic = {}
	# step-number
	m = re.search(r'(\d+)\s+X-axis Step Number \[1~1024\]', buffer)
	if m:
		x_step_number = int(m.group(1))
		dic['x_step_number'] = x_step_number
		m = re.search(r'(\S+)\s+X Step Size \[um\]', buffer)
		if m:
			x_step_size = float(m.group(1))
			dic['x_step_size'] = x_step_size
			width_in_um = x_step_size * x_step_number
			dic['magnification'] = _magnification(width_in_um)

	m = re.search(r'(\d+)\s+Y-axis Step Number \[1~1024\]', buffer)
	if m:
		dic['y_step_number'] = int(m.group(1))

	m = re.search(r'(\S+)\s+Y Step Size \[um\]', buffer)
	if m:
		dic['y_step_size'] = float(m.group(1))

	m = re.search(r'(\S)\s+Stage\[S\] or Beam\[B\] Scan', buffer)
	if m:
		dic['scan_mode'] = m.group(1)


	m = re.search(r'(\S+)\s+Measurement Center Position X \[mm\]', buffer)
	if m:
		dic['x_stage_position'] = m.group(1)
	m = re.search(r'(\S+)\s+Measurement Center Position Y \[mm\]', buffer)
	if m:
		dic['y_stage_position'] = m.group(1)
	m = re.search(r'(\S+)\s+Measurement Center Position Z \[mm\]', buffer)
	if m:
		dic['z_stage_position'] = m.group(1)

	wds_cond_name = ""
	m = re.search(r'(\S+)\s+Element Name', buffer)
	if m:
		header = buffer[0:m.start()]
		dic['comment'] = header.split("\n")[-3].strip()
		wds_cond_name += m.group(1)
		dic['element_name'] = m.group(1)
	m = re.search(r'(\S+)\s+Channel Number', buffer)
	if m:
		wds_cond_name += "_CH" + m.group(1)
		dic['channel_name'] = "CH" + m.group(1)
	m = re.search(r'(\S+)\s+Crystal Name', buffer)
	if m:
		wds_cond_name += "_" + m.group(1)
		dic['crystal_name'] = m.group(1)

	m = re.search(r'(\S+)\s+X-ray Name', buffer)
	if m:
		wds_cond_name += "_" + m.group(1)
		dic['x_ray_name'] = m.group(1)
	dic['signal'] = wds_cond_name
	return dic

def _parse_condition(buffer):
	if re.match(r'\$', buffer):
		return _parse_condition_feepma(buffer)
	else:
		return _parse_condition_jxa1(buffer)

def _read_condition_0(path, elem_idx):
	buffer = open(path, 'r').read()
	tokens = []
	idx = 0
	for m in re.finditer(r'(\S+)\s+Element Name No\.(\d+)-Seq\.(\d+) \*+', buffer):
		tokens.append(buffer[idx:m.start()])
		idx = m.start()
	tokens.append(buffer[idx:-1])
	header = tokens[0]
	element = tokens[elem_idx]	
	return header + element

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
		if os.path.exists(cnd_path):
			buffer = open(cnd_path, 'r').read()
		elif os.path.exists(cnd_path_0):
			buffer = _read_condition_0(cnd_path_0, 1)
			#buffer = open(cnd_path_0, 'r').read()
	return buffer

def _get_condition(path, **options):
	buffer = _read_condition(path, **options)
	if buffer:
		return _parse_condition(buffer)

