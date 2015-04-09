import sys
import os
from nose.tools import *
from jxmap.commands import _parse_options, map2tiff, map2raw, map2jpeg

saved = None

def setup():
	global saved
	saved = sys.argv

def teardown():
	sys.argv = saved

@with_setup(setup, teardown)
def test_options():
	sys.argv = ['map2tiff', '--byte-order', 'big-endian']
	options, args = _parse_options()
	assert_equals(options.byte_order, 'big-endian')

def test_map2tiff():
	map2tiff()

def test_map2jpeg():
	map2jpeg()

def test_map2raw():
	map2raw()
