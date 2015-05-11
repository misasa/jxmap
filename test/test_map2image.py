import sys
import os
import numpy
import shutil
import re
from nose.tools import *
from jxmap.map2image import map2image, _parse_options, _get_rpl_text

files_dir = os.path.join(os.path.dirname(__file__), 'files')
saved = None

def setup_tmp():
	if os.path.exists('tmp'):
		shutil.rmtree('tmp')
	os.mkdir('tmp')

def setup():
	setup_tmp()
	global saved
	saved = sys.argv

def teardown():
	sys.argv = saved

def test_options():
	sys.argv = ['map2tiff', '--swap-byte', '--offset', '32', '--geometry', '920x1000', 'tmp/7.map', 'tmp/7.tiff']
	options, args = _parse_options()
	assert_equals(options.swap_byte, True)
	assert_equals(options.offset, 32)
	assert_equals(options.step_numbers, (920,1000))

def test_options_without_geometry():
	sys.argv = ['map2tiff', 'tmp/7.map', 'tmp/7.tiff']
	options, args = _parse_options()
	assert_equals(options.step_numbers, None)

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

@with_setup(setup, teardown)
def test_with_invalid_condition_path():
	shutil.copy(os.path.join(files_dir, '7.map'),'tmp')
 	sys.argv = ['map2tiff', '--condition-file', 'example.cnd', 'tmp/7.map', 'tmp/7.raw']
	assert_raises(RuntimeError, map2image)

@with_setup(setup, teardown)
def test_map2iamge_jpeg():
	os.mkdir('tmp/jpeg')
	shutil.copy(os.path.join(files_dir, 'data003.map'),'tmp')
	shutil.copy(os.path.join(files_dir, 'data003.cnd'),'tmp')	
	sys.argv = ['map2jpeg', 'tmp/data003.map', 'tmp/jpeg/data003.jpeg']
	map2image()
	assert_true(os.path.exists('tmp/jpeg/data003.jpeg'))
	assert_true(os.path.exists('tmp/jpeg/data003.txt'))

@with_setup(setup, teardown)
def test_map2iamge_jpeg_2():
	os.mkdir('tmp/jpeg')
	shutil.copy(os.path.join(files_dir, 'OK10VM-a.map'),'tmp')
	shutil.copy(os.path.join(files_dir, 'OK10VM-a.cnd'),'tmp')	
	sys.argv = ['map2jpeg', 'tmp/OK10VM-a.map', 'tmp/jpeg/OK10VM-a.jpeg']
	map2image()
	assert_true(os.path.exists('tmp/jpeg/OK10VM-a.jpeg'))
	assert_true(os.path.exists('tmp/jpeg/OK10VM-a.txt'))


@with_setup(setup, teardown)
def test_map2iamge_tiff():
	os.mkdir('tmp/jpeg')
	shutil.copy(os.path.join(files_dir, 'data006.map'),'tmp')
	shutil.copy(os.path.join(files_dir, 'data006.cnd'),'tmp')	
	sys.argv = ['map2jpeg', 'tmp/data006.map', 'tmp/jpeg/data006.tiff']
	map2image()
	assert_true(os.path.exists('tmp/jpeg/data006.tiff'))
	assert_true(os.path.exists('tmp/jpeg/data006.txt'))
#	assert_true(os.path.exists('tmp/jpeg/data006.info'))

def test_map2image_raw():
	os.mkdir('tmp/raw')
	shutil.copy(os.path.join(files_dir, 'data003.map'),'tmp')	
	shutil.copy(os.path.join(files_dir, 'data003.cnd'),'tmp')	
	sys.argv = ['map2raw', 'tmp/data003.map', os.path.abspath('tmp/raw/data003.raw')]
	map2image()
	assert_true(os.path.exists('tmp/raw/data003.raw'))
	assert_true(os.path.exists('tmp/raw/data003.rpl'))
	assert_true(os.path.exists('tmp/raw/data003.txt'))


@with_setup(setup, teardown)
def test_map2iamge_jpeg_OK10VM():
	os.mkdir('tmp/jpeg')
	shutil.copy(os.path.join(files_dir, 'OK10VM-a-2.map'),'tmp')
	shutil.copy(os.path.join(files_dir, 'OK10VM-a-2.cnd'),'tmp')	
	sys.argv = ['map2jpeg', 'tmp/OK10VM-a-2.map', 'tmp/jpeg/OK10VM-a-2.jpeg']
	map2image()
	assert_true(os.path.exists('tmp/jpeg/OK10VM-a-2.jpeg'))
	assert_true(os.path.exists('tmp/jpeg/OK10VM-a-2.txt'))

#@with_setup(setup, teardown)
def test_map2iamge_jpeg_ProbeScan():
	#os.mkdir('tmp/jpeg')
	shutil.copy(os.path.join(files_dir, 'ProbeScan.map'),'tmp')
	shutil.copy(os.path.join(files_dir, 'ProbeScan.cnd'),'tmp')	
	sys.argv = ['map2jpeg', 'tmp/ProbeScan.map', 'tmp/jpeg/ProbeScan.jpeg']
	map2image()
	assert_true(os.path.exists('tmp/jpeg/ProbeScan.jpeg'))
	assert_true(os.path.exists('tmp/jpeg/ProbeScan.txt'))

