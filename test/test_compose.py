import sys
import os
import numpy
import shutil
import re
from nose.tools import *
from jxmap.compose import compose

files_dir = os.path.join(os.path.dirname(__file__), 'files')
saved = None

def setup_tmp():
	if os.path.exists('tmp'):
		shutil.rmtree('tmp')
	os.mkdir('tmp')
	shutil.copy(os.path.join(files_dir, 'OK10VM-a-2.map'),'tmp')
	shutil.copy(os.path.join(files_dir, 'OK10VM-a-2.cnd'),'tmp')	
	shutil.copy(os.path.join(files_dir, 'data006.map'),'tmp')
	shutil.copy(os.path.join(files_dir, 'data006.cnd'),'tmp')	


def setup():
	setup_tmp()
	global saved
	saved = sys.argv

def teardown():
	sys.argv = saved

@with_setup(setup, teardown)
def test_compose():
	sys.argv = ['compose', 'tmp/OK10VM-a-2.map', 'tmp/data006.map']
	compose()
