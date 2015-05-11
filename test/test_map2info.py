import sys
import os
import numpy
import shutil
import re
from nose.tools import *
# from jxmap.commands import _get_rpl_text, _get_info_text
# from jxmap.commands import _dtype
# from jxmap.commands import _read_map
# from jxmap.commands import _parse_options
from jxmap.map2info import *
# from jxmap.commands import _cnd_path, _cnd_path_0
# from jxmap.commands import _read_condition, _read_condition_0, _parse_condition
# from jxmap.commands import _magnification

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

@with_setup(setup, teardown)
def test_map2info_jpeg_3():
	shutil.copy(os.path.join(files_dir, 'OK10VM-a-2.map'),'tmp')
	shutil.copy(os.path.join(files_dir, 'OK10VM-a-2.cnd'),'tmp')	
	sys.argv = ['map2info', 'tmp/OK10VM-a-2.map']
	map2info()


def test_map2info():
	shutil.copy(os.path.join(files_dir, 'ProbeScan.map'),'tmp')
	shutil.copy(os.path.join(files_dir, 'ProbeScan.cnd'),'tmp')	
	sys.argv = ['map2info', 'tmp/ProbeScan.map']
	map2info()
