import sys
import os
import numpy
import shutil
import re
from nose.tools import *
from jxmap.u8raw import u8raw
from jxmap.map2image import map2image

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



def test_raw():
	os.mkdir('tmp/raw')
	shutil.copy(os.path.join(files_dir, 'data003.map'),'tmp')	
	shutil.copy(os.path.join(files_dir, 'data003.cnd'),'tmp')	
	sys.argv = ['map2raw', 'tmp/data003.map', os.path.abspath('tmp/raw/data003.raw')]
	map2image()
	assert_true(os.path.exists('tmp/raw/data003.raw'))
	assert_true(os.path.exists('tmp/raw/data003.rpl'))
	assert_true(os.path.exists('tmp/raw/data003.txt'))
	sys.argv = ['map2raw', 'tmp/raw/data003.raw']
	u8raw()

