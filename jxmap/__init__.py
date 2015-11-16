#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
import numpy
import pickle
import matplotlib
import PIL

__version__ = '0.0.8'

def byteorder(rpl):
	o = ""
	if rpl["byte-order"] == "big-endian":
		o = ">"
	elif rpl["byte-order"] == "little-endian":
		o = "<"
	
	return o

def load_rpl(rpl_path):
	rpl = {}
	f = open(rpl_path, 'rb')
	buffer = f.read()
	key_vals = buffer.split('\n')
	for key_val in key_vals:
		if key_val != "":
			key, val = key_val.split('\t')
			rpl[key] = val
	f.close()
	return rpl

def load_raw(path, rpl):
	width = rpl["width"]
	height = rpl["height"]
	dtype = 'u1'
	
	if int(rpl["data-length"]) == 2:
		dtype = byteorder(rpl) + 'u2' 
	elif int(rpl["data-length"]) == 4:
		dtype = byteorder(rpl) + 'u4' 
	elif int(rpl["data-length"]) == 8:
		dtype = byteorder(rpl) + 'f8' 
	
	return numpy.fromfile(path, dtype=dtype,count=int(width)*int(height))

def load_pickle(pkl_path):
	f_pickle = open(pkl_path, 'rb')
	imlist = pickle.load(f_pickle)
	numphase = pickle.load(f_pickle)
	centroids = pickle.load(f_pickle)
	variance = pickle.load(f_pickle)
	code = pickle.load(f_pickle)
	distance = pickle.load(f_pickle)

	setting = {}
	setting['imlist'] = imlist
	setting['numphase'] = numphase
	setting['centroids'] = centroids
	setting['variance'] = variance
	setting['code'] = code
	setting['distance'] = distance
	
	return PhaseMap(setting)


class PhaseMap():
	def __init__(self, setting):
		self.colors = ["Red", "Green", "Blue", "Yellow", "Magenta", "Cyan", "Dark Orange", "Light Green", "Dark Green", "Light Blue", "Brown", "Light Yellow", "Violet", "Tan", "Sky Blue"]
		self.plot_colors = [color.replace(' ','').lower() for color in self.colors]
		self.plot_rgbs = []
		
		for color in self.plot_colors:
			rgb = matplotlib.colors.ColorConverter().to_rgb(color)
			self.plot_rgbs.append([int(f * 255) for f in rgb])
		
		self.setting = setting
		self.imlist = setting['imlist']
		self.numphase = setting['numphase']
		self.centroids = setting['centroids']
		self.variance = setting['variance']
		self.code = setting['code']
		self.distance = setting['distance']
#		self.features = features
		self.element_names = [ os.path.splitext(imname)[0] for imname in self.imlist ]


		self.load_features()
		
		hs = []
		pixel_sum = 0
		for idx in range(len(self.centroids)):
			h = {}
			locs = numpy.where(self.code == idx)[0]
			
			t = []
			for element_idx in range(len(self.element_names)): 
				fs = self.features[locs, element_idx]
				t.append( [ numpy.min(fs), numpy.max(fs), numpy.mean(fs) ] )
			
			h['code'] = idx
			h['centroid'] = self.centroids[idx]
			h['sum_centroid'] = sum(h['centroid'])
			h['pixel_count'] = len(locs)
			h['intensity_range'] = t
			pixel_sum += h['pixel_count']
			hs.append(h)
		
		phase_in_lisps = []
		for h in hs:
			h['pixel_percent'] = h['pixel_count']/float(pixel_sum) * 100
		
		sorted_hs = sorted(hs, key=lambda h: h['sum_centroid'])
		sorted_hs.reverse()
		self.table = sorted_hs
	
	def load_features(self):
		raw_path = self.imlist[0]
		root, ext = os.path.splitext(raw_path)
		dirname = os.path.dirname(raw_path)
		rpl_path = os.path.join(dirname, os.path.basename(root) + '.rpl')
		rpl = load_rpl(rpl_path)
		self.width = int(rpl['width'])
		self.height = int(rpl['height'])

		ims = []
		for path in self.imlist:
			root, ext = os.path.splitext(path)
			dirname = os.path.dirname(path)
			rpl_path = os.path.join(dirname, os.path.basename(root) + '.rpl')
			tmp_rpl = load_rpl(rpl_path)
			ims = numpy.append(ims, load_raw(path, tmp_rpl))	
			#ims = numpy.append(ims, numpy.fromfile(path, dtype='<u2',count=int(self.width)*int(self.height)))	
		self.features = ims.reshape(len(self.imlist), int(self.width)*int(self.height)).transpose()	
		
	
	def show_table(self, out):
		element_names = self.element_names
		sorted_hs = self.table
		colors = self.colors
		header = "%8s" % "name" + "%15s" % "color" + "%5s" % "code"  + "%10s" % "area (%)"
		for element_idx in range(len(self.element_names)):
			header += "%10s" % self.element_names[element_idx]
		#	header += " [%5s - %5s (%10s)] " % ("min", "max", "mean")
		header += "%10s" % "sum"
		out.write(header + "\n")
		for idx in range(len(sorted_hs)):
			h = sorted_hs[idx]
			centroid = h['centroid']
			intensity_range = h['intensity_range']
			line = "Phase-%02d" % idx + "%15s" % colors[idx % len(colors)] + "%5d" % h['code'] + "%10.2f" % h['pixel_percent']
			for element_idx in range(len(element_names)):
				mean = centroid[element_idx]
				line += "%10.2f" % mean
		#		line += " [%5d - %5d (%10.2f)] " % (intensity_range[element_idx][0], intensity_range[element_idx][1], intensity_range[element_idx][2] )
			line += "%10.2f" % h['sum_centroid']
			out.write(line + "\n")
		
	
	def dump_lisp(self, path, root_name):
		sorted_hs = self.table
		element_names = self.element_names
		phase_in_lisps = []
		for idx in range(len(sorted_hs)):
			h = sorted_hs[idx]	
			lisp = "(\"Phase-%02d\" ((\"%s\" %d %d %.5f)) %.5f :and \"%s\")" % (idx, root_name, h['code'], h['code'], h['pixel_percent'], h['pixel_percent'], self.colors[idx % len(self.colors)])
			phase_in_lisps.append(lisp)

		lisp = open(path, 'w')
		lisp.write("(" + "\n".join(phase_in_lisps) + ")\n")
		lisp.write("(16711680 \"Phase-00\"\n(" + "\n".join([ "(\"Phase-%02d\" \"%s\")" % (idx, root_name) for idx in range(len(self.centroids)) ]) + "))\n")
		lisp.write("(" + " ".join([ "\"%s\"" % element_name for element_name in element_names]) + (" \"%s\"" % root_name) + ")\n")
		lisp.close()

	def dump_raw(self, default_raw_path):
		numpy.array(self.code).astype('int16').tofile(default_raw_path)
		
	def dump_image(self, default_image_path):
		codeim = self.code.reshape(self.height,self.width)
		yPix, xPix = codeim.shape
		data = numpy.zeros( (yPix,xPix,3), dtype=numpy.uint8)
		for i in range(len(self.table)):
			data[numpy.where(codeim == i)] = self.plot_rgbs[i]

		img = PIL.Image.fromarray(data, 'RGB')
		img.save(default_image_path)
		
		#print self.plot_rgbs
		
		#numpy.array(self.code).astype('int16').tofile(default_raw_path)
	
	def dump_rpl(self, default_rpl_path):
		rpl = open(default_rpl_path, 'w')
		rpl.write("key\tvalue\n")
		rpl.write("width\t%d\n" % self.width)
		rpl.write("height\t%d\n" % self.height)
		rpl.write("depth\t%d\n" % 1)
		rpl.write("offset\t%d\n" % 0)
		rpl.write("data-length\t%d\n" % 2)
		rpl.write("data-type\tunsigned\n")
		rpl.write("byte-order\tlittle-endian\n")
		rpl.write("record-by\timage\n")
		rpl.close()
	
	# def show_figure(self):
	# 	print self.code
	# 	codeim = self.code.reshape(self.height,self.width)
	# 	figure()
	# 	gray()
	# 	axis('off')
	# 	imshow(codeim)
	# 	show()


class Jxmap(object):
	class_var = "hoge"
	@classmethod
	def read_map(cls, path, x_step_number, y_step_number, **options):
		file_size = os.path.getsize(path)
		f = open(path, 'rb') 
		buffer = f.read()
		data_count = x_step_number * y_step_number
		bytes_per_data = file_size / data_count

		offset = file_size - data_count * bytes_per_data
		if options.get('offset', False):
			offset = options.get('offset')
		#print "%s %dx%d %d %d %d" % (path, x_step_number, y_step_number, file_size, offset, bytes_per_data)
		dtype = cls.get_dtype(bytes_per_data)

		imgArray = numpy.frombuffer(buffer, dtype=dtype, count=data_count, offset=offset).copy()

		if options.get('swap_byte', False):
			imgArray.byteswap(True)

		if options.get('scan_mode', 'S') == 'B':
			imgArray = imgArray.reshape((y_step_number, x_step_number)).copy()
		else:
			imgArray = imgArray.reshape((x_step_number, y_step_number)).copy()
			imgArray = numpy.rot90(imgArray, 3).copy()

		return imgArray

	@classmethod
	def get_dtype(cls, bytes_per_data):
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

	@classmethod
	def read_cnd0_file(cls, path, elem_idx = 1):
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
	@classmethod
	def parse_condition(cls, buffer):
		if re.match(r'\$', buffer):
			return cls.parse_condition_jxa8530f(buffer)
		else:
			return cls.parse_condition_jxa8800(buffer)

	@classmethod
	def magnification(cls, width_in_um):
		return 120000/float(width_in_um)

	@classmethod
	def parse_condition_jxa8530f(cls, buffer):
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
				dic['magnification'] = cls.magnification(width_in_um)

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
			if len(vals) > 1:
				dic['channel_name'] = vals[1]
			if len(vals) > 2:
				dic['crystal_name'] = vals[2]
			if len(vals) > 3:
				dic['x_ray_name'] = vals[3]

		m = re.search(r'\$XM_ELEM_WDS_CRYSTAL_NAME%(\d+) (\S+)', buffer)
		if m:
			dic['crystal_name'] = m.group(2)


		m = re.search(r'\$XM_ELEM_WDS_XRAY%(\d+) (\S+)', buffer)
		if m:
			dic['x_ray_name'] = m.group(2)


		m = re.search(r'\$XM_ELEM_IMS_SIGNAL_TYPE%(\d+) (\S+)', buffer)
		if m:
			dic['signal'] = m.group(2)

		return dic


	@classmethod
	def parse_condition_jxa8800(cls, buffer):
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
				dic['magnification'] = cls.magnification(width_in_um)

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



	def __init__(self, **kargs):
		self.map_path = kargs.get('map_path', None)
		self.cnd_path = kargs.get('cnd_path', None)
		if self.map_path:
			buffer = self.read_cnd_file()
			if buffer:
				self.condition = self.__class__.parse_condition(buffer)
		else:			
			self.condition = kargs.get('condition', {})
#			self.center = kargs.get('center',(0, 0))
#			self.step_number = kargs.get('step_number',(0, 0))
#			self.step_size = kargs.get('step_size',(0.0, 0.0))
#			self.size = (self.step_size[0] * self.step_number[0], self.step_size[1] * self.step_number[1])

	def root(self):
		root, org_ext = os.path.splitext(self.map_path)
		return root

	def basename(self):
		return os.path.basename(self.root())

	def dirname(self):
		return os.path.dirname(self.root())

	def _cnd_path(self):
		return os.path.join(self.dirname(), self.basename() + '.cnd')

	def _cnd_path_0(self):
		return os.path.join(self.dirname(), '0.cnd')

	def load_map(self, **options):
		self.data = self.__class__.read_map(self.map_path, x_step_number = self.condition.get('x_step_number'), y_step_number = self.condition.get('y_step_number'), **options)

	def read_cnd_file(self):
		buffer = None
		if self.cnd_path:
			cnd_path = os.path.abspath(self.cnd_path)
			if os.path.exists(cnd_path):
				buffer = open(cnd_path, 'r').read()
			else:
				raise RuntimeError, "could not find %s" % cnd_path
		else:
			cnd_path = self._cnd_path()
			cnd_path_0 = self._cnd_path_0()
			if os.path.exists(cnd_path):
				self.cnd_path = cnd_path
				buffer = open(cnd_path, 'r').read()
			elif os.path.exists(cnd_path_0):
				self.cnd_path = cnd_path_0
				print self.__class__
				buffer = self.__class__.read_cnd0_file(cnd_path_0, 1)
		return buffer

	def sem_info(self):
		if not self.condition:
			return

		con = self.condition
		info = "$CM_TITLE %s %s\n" % (con.get('comment', 'map'), con.get('signal', 'signal'))
		info += "$CM_MAG %.0f\n" % con.get('magnification', 1)
		info += "$CM_FULL_SIZE %d %d\n" % (con.get('x_step_number', 0), con.get('y_step_number', 0))
		info += "$CM_STAGE_POS %s %s %s 0 0 0\n" % (con.get('x_stage_position', '0'), con.get('y_stage_position', '0'), con.get('z_stage_position', '0'))
		info += "$$SM_SCAN_ROTATION 0.00\n"
		return info

