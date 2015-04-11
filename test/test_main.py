import sys
import os
import numpy
import shutil
import re
from nose.tools import *
from jxmap.commands import _get_rpl_text
from jxmap.commands import _dtype
from jxmap.commands import _read_map
from jxmap.commands import _parse_options
from jxmap.commands import map2image
from jxmap.commands import _cnd_path, _cnd_path_0
from jxmap.commands import _read_condition, _parse_condition

saved = None

files_dir = os.path.join(os.path.dirname(__file__), 'files')
mapfile = os.path.join('tmp', 'big-920x1000.map')
mapfile2 = os.path.join('tmp', 'little-1800x1600.map')
mapfile_003 = os.path.join('tmp', 'data003.map')
mapfile_7 = os.path.join('tmp', '7.map')
def setup_tmp():
	if os.path.exists('tmp'):
		shutil.rmtree('tmp')
	os.mkdir('tmp')

def setup():
	setup_tmp()
	# shutil.copy(os.path.join(files_dir, 'big-920x1000.map'),'tmp')
	# shutil.copy(os.path.join(files_dir, 'little-1800x1600.map'),'tmp')
	# shutil.copy(os.path.join(files_dir, 'data003.map'),'tmp')
	# shutil.copy(os.path.join(files_dir, 'data003.cnd'),'tmp')
	# shutil.copy(os.path.join(files_dir, '7.map'),'tmp')
	# shutil.copy(os.path.join(files_dir, '0.cnd'),'tmp')

	global saved
	saved = sys.argv

def teardown():
	sys.argv = saved

@with_setup(setup, teardown)
def test_options():
	sys.argv = ['map2tiff', '--swap-byte', '--offset', '32', '--geometry', '920x1000', 'tmp/7.map', 'tmp/7.tiff']
	options, args = _parse_options()
	assert_equals(options.swap_byte, True)
	assert_equals(options.offset, 32)
	assert_equals(options.step_numbers, (920,1000))

@with_setup(setup, teardown)
def test_options_without_geometry():
	shutil.copy(os.path.join(files_dir, '7.map'),'tmp')
	shutil.copy(os.path.join(files_dir, '0.cnd'),'tmp')

	sys.argv = ['map2tiff', 'tmp/7.map', 'tmp/7.tiff']
	options, args = _parse_options()
	assert_equals(options.step_numbers, (920,1000))


def test_dtype():
	assert_equals(_dtype(2), 'u2')
	assert_equals(_dtype(4), 'u4')
	assert_equals(_dtype(8), 'f8')
	assert_raises(RuntimeError, _dtype, 1)
	assert_raises(RuntimeError, _dtype, 9)


def test_get_rpl_text():
	x_step_number = 920
	y_step_number = 1000
	imgArray = numpy.zeros((y_step_number, x_step_number), dtype=numpy.uint16)
	rpl = _get_rpl_text(imgArray)
	assert_true(re.search("data-length\t2", rpl))
	assert_true(re.search("data-type\tunsigned", rpl))

	imgArray = numpy.zeros((y_step_number, x_step_number), dtype=numpy.uint32)
	rpl = _get_rpl_text(imgArray)
	assert_true(re.search("data-length\t4", rpl))
	assert_true(re.search("data-type\tunsigned", rpl))

	imgArray = numpy.zeros((y_step_number, x_step_number), dtype=numpy.float64)
	rpl = _get_rpl_text(imgArray)
	assert_true(re.search("data-length\t8", rpl))
	assert_true(re.search("data-type\tfloat", rpl))

	imgArray = numpy.zeros((y_step_number, x_step_number), dtype=numpy.uint8)
	rpl = _get_rpl_text(imgArray)
	assert_true(re.search("data-length\t1", rpl))
	assert_true(re.search("data-type\tunsigned", rpl))

def setup_cnd():
	setup()
	tmp_path = _cnd_path(mapfile)
	f = open(tmp_path, "w")
	f.write(tmp_path)

def setup_cnd_0():
	setup()
	tmp_path = _cnd_path_0(mapfile)
	f = open(tmp_path, "w")
	f.write(tmp_path)

@with_setup(setup, teardown)
def test_read_condition_003():
	assert_equal(_read_condition(mapfile_003), None)

@with_setup(setup, teardown)
def test_with_invalid_condition_path():
 	sys.argv = ['map2tiff', '--condition-file', 'example.cnd', 'tmp/7.map', 'tmp/7.raw']
	assert_raises(RuntimeError, _parse_options)

def test_parse_condition_0():
	cnd_path = os.path.join(files_dir, '0.cnd')
	buffer = open(cnd_path).read()
	con = _parse_condition(buffer)
	assert_equal(con['x_step_number'], 920)
	assert_equal(con['y_step_number'], 1000)

def test_parse_condition_003():
	cnd_path = os.path.join(files_dir, 'data003.cnd')
	buffer = open(cnd_path).read()
	con = _parse_condition(buffer)
	assert_equal(con['x_step_number'], 1800)
	assert_equal(con['y_step_number'], 1600)


@with_setup(setup, teardown)
def test_read_map_7():
	shutil.copy(os.path.join(files_dir, '7.map'),'tmp')
	imgArray1 = _read_map('tmp/7.map', x_step_number = 920, y_step_number =1000, swap_byte = True)
	assert_equals(imgArray1.shape, (1000, 920))
	assert_equals(numpy.amax(imgArray1), 1005)

@with_setup(setup, teardown)
def test_read_map_003():
	shutil.copy(os.path.join(files_dir, 'data003.map'),'tmp')
	imgArray2 = _read_map('tmp/data003.map', x_step_number = 1800, y_step_number = 1600)
	assert_equals(imgArray2.shape, (1600, 1800))
	assert_equals(numpy.amax(imgArray2), 67.0)

@with_setup(setup, teardown)
def test_map2iamge_jpeg():
	os.mkdir('tmp/jpeg')
	shutil.copy(os.path.join(files_dir, 'data003.map'),'tmp')	
	shutil.copy(os.path.join(files_dir, 'data003.cnd'),'tmp')	
	sys.argv = ['map2jpeg', 'tmp/data003.map', 'tmp/jpeg/data003.jpeg']
	map2image()
	assert_true(os.path.exists('tmp/jpeg/data003.jpeg'))

def test_map2image_raw():
	os.mkdir('tmp/raw')
	shutil.copy(os.path.join(files_dir, 'data003.map'),'tmp')	
	shutil.copy(os.path.join(files_dir, 'data003.cnd'),'tmp')	
	sys.argv = ['map2raw', 'tmp/data003.map', os.path.abspath('tmp/raw/data003.raw')]
	map2image()
	assert_true(os.path.exists('tmp/raw/data003.raw'))
	assert_true(os.path.exists('tmp/raw/data003.rpl'))
