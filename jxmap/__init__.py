#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
import numpy

__version__ = '0.0.6'

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
	print rpl
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
			dic['channel_name'] = vals[1]
			dic['crystal_name'] = vals[2]
			dic['x_ray_name'] = vals[3]
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

