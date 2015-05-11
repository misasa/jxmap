import sys
import os
import shutil
from nose.tools import *
from jxmap import __version__ as VERSION

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

def test_version():
	assert_equal(VERSION, '0.0.4')
