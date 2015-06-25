import sys
import os
import numpy
import shutil
import re
from nose.tools import *
from jxmap.phase_analysis import phase_analysis_kmeans, map_create
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



def test_kmeans():
	os.mkdir('tmp/raw')

	shutil.copy(os.path.join(files_dir, 'data003.map'),'tmp')	
	shutil.copy(os.path.join(files_dir, 'data003.cnd'),'tmp')	
	sys.argv = ['map2raw', 'tmp/data003.map', os.path.abspath('tmp/raw/data003.raw')]
	map2image()
	shutil.copy(os.path.join(files_dir, 'data006.map'),'tmp')	
	shutil.copy(os.path.join(files_dir, 'data006.cnd'),'tmp')	
	sys.argv = ['map2raw', 'tmp/data006.map', os.path.abspath('tmp/raw/data006.raw')]
	map2image()

	sys.argv = ['phase-analysis-kmeans', 'tmp/raw/data003.raw', 'tmp/raw/data006.raw']
	phase_analysis_kmeans()
	sys.argv = ['phase-map-create', 'tmp/raw/phases-5.pkl']
	map_create()
