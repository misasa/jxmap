import sys
import os
import numpy
import shutil
from nose.tools import *
from jxmap.commands import _dtype, _read_map, _parse_options, map2tiff, map2raw, map2jpeg

saved = None

files_dir = os.path.join(os.path.dirname(__file__), 'files')
mapfile = os.path.join('tmp', 'big-920x1000.map')
mapfile2 = os.path.join('tmp', 'little-1800x1600.map')

def setup():
	if os.path.exists('tmp'):
		shutil.rmtree('tmp')
	os.mkdir('tmp')
	shutil.copy(os.path.join(files_dir, 'big-920x1000.map'),'tmp')
	shutil.copy(os.path.join(files_dir, 'little-1800x1600.map'),'tmp')	

	global saved
	saved = sys.argv



def teardown():
	sys.argv = saved

@with_setup(setup, teardown)
def test_options():
	sys.argv = ['map2tiff', '--swap-byte', '--offset', '32']
	options, args = _parse_options()
	assert_equals(options.swap_byte, True)
	assert_equals(options.offset, 32)

@with_setup(setup, teardown)
def test_read_map():
	imgArray1 = _read_map(mapfile, 920, 1000, swap_byte = True)
#	assert_equals(imgArray1.shape, (920, 1000))
	assert_equals(numpy.amax(imgArray1), 1005)

	imgArray2 = _read_map(mapfile2, 1800, 1600)
#	assert_equals(imgArray2.shape, (1800, 1600))
	assert_equals(numpy.amax(imgArray2), 67.0)

def test_dtype():
	assert_equals(_dtype(2), 'u2')
	assert_equals(_dtype(4), 'u4')
	assert_equals(_dtype(8), 'f8')
	assert_raises(RuntimeError, _dtype, 1)
	assert_raises(RuntimeError, _dtype, 9)

@with_setup(setup, teardown)
def test_map2tiff():
	sys.argv = ['map2tiff', '--swap-byte', mapfile, '920', '1000']
	map2tiff()

@with_setup(setup, teardown)
def test_map2jpeg():
	sys.argv = ['map2jpeg', '--swap-byte', mapfile, '920', '1000']
	map2jpeg()

@with_setup(setup, teardown)
def test_map2tiff_with_offset():
	sys.argv = ['map2tiff', '--swap-byte', mapfile, '920', '1000']
	map2tiff()
# @with_setup(setup, teardown)
# def test_map2raw():
# 	sys.argv = ['map2raw', '--swap-byte', mapfile, '920', '1000']
# 	map2raw()