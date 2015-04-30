import sys
import os
import numpy
import shutil
import re
from nose.tools import *
from jxmap.commands import _get_rpl_text, _get_info_text
from jxmap.commands import _dtype
from jxmap.commands import _read_map
from jxmap.commands import _parse_options
from jxmap.commands import map2image, map2info
from jxmap.commands import _cnd_path, _cnd_path_0
from jxmap.commands import _read_condition, _read_condition_0, _parse_condition
from jxmap.commands import _magnification

saved = None

files_dir = os.path.join(os.path.dirname(__file__), 'files')
mapfile = os.path.join('tmp', 'big-920x1000.map')
mapfile2 = os.path.join('tmp', 'little-1800x1600.map')
mapfile_003 = os.path.join('tmp', 'data003.map')
mapfile_006 = os.path.join('tmp', 'data006.map')
mapfile_7 = os.path.join('tmp', '7.map')
mapfile_ok10vm_a = os.path.join('tmp', 'OK10VM-a.map')

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

def test_get_magnification():
	assert_equal(_magnification(240000.0), 0.5)
	assert_equal(_magnification(120000.0), 1.0)
	assert_equal(_magnification(60000.0), 2.0)

def test_get_info_text():
	buffer = '''
920      X-axis Step Number [1~1024]
1000     Y-axis Step Number [1~1024]
4.0      X Step Size [um]
-20.8380 Measurement Center Position X [mm]
16.8980  Measurement Center Position Y [mm]
10.7432  Measurement Center Position Z [mm]
Hello World                                
Apr 4 06:52 2013
F                       Element Name No.1-Seq.1 **********
Ka                      X-ray Name
1                       X-ray Order
W                       Signal Name [W:WDS E:EDS I:IMS]
1                       Channel Number[1-5:WDS 8-15:EDS 6,7:IMS]
TAP                             Crystal Name
1                       Crystal Number
'''
	con = _parse_condition(buffer)
	text = _get_info_text(con)
	assert_true(re.search(r'\$CM_TITLE Hello World F_CH1_TAP_Ka', text))	
	assert_true(re.search(r'\$CM_MAG (\d+)', text))
	assert_true(re.search(r'\$CM_FULL_SIZE 920 1000', text))		
	assert_true(re.search(r'\$CM_STAGE_POS -20\.8380 16\.8980 10\.7432 0 0 0', text))
	assert_true(re.search(r'\$\$SM_SCAN_ROTATION 0\.00', text))

def test_parse_condition_jxa():
	buffer = '''
920      X-axis Step Number [1~1024]
1000     Y-axis Step Number [1~1024]
4.0      X Step Size [um]
4.0      Y Step Size [um]
S			Stage[S] or Beam[B] Scan
-20.8380 Measurement Center Position X [mm]
16.8980  Measurement Center Position Y [mm]
10.7432  Measurement Center Position Z [mm]
Hello World                                
Apr 4 06:52 2013
F                       Element Name No.1-Seq.1 **********
Ka                      X-ray Name
1                       X-ray Order
W                       Signal Name [W:WDS E:EDS I:IMS]
1                       Channel Number[1-5:WDS 8-15:EDS 6,7:IMS]
TAP                             Crystal Name
1                       Crystal Number
'''
	con = _parse_condition(buffer)
	assert_equal(con['x_step_number'], 920)
	assert_equal(con['y_step_number'], 1000)
	assert_equal(con['x_step_size'], 4.0)
	assert_equal(con['y_step_size'], 4.0)
	assert_equal(con['magnification'], 120000/920.0/4.0)
	assert_equal(con['x_stage_position'], '-20.8380')
	assert_equal(con['y_stage_position'], '16.8980')
	assert_equal(con['z_stage_position'], '10.7432')
	assert_equal(con['comment'], 'Hello World')
	assert_equal(con['signal'], 'F_CH1_TAP_Ka')
	assert_equal(con['element_name'], 'F')
	assert_equal(con['channel_name'], 'CH1')
	assert_equal(con['crystal_name'], 'TAP')
	assert_equal(con['x_ray_name'], 'Ka')
	assert_equal(con['scan_mode'], 'S')


def test_parse_condition_0():
	cnd_path = os.path.join(files_dir, '0.cnd')
	buffer = _read_condition_0(cnd_path, 7)
	con = _parse_condition(buffer)
	assert_true(con['x_step_number'])
	assert_true(con['y_step_number'])
	assert_true(con['x_step_size'])
	assert_true(con['y_step_size'])	
	assert_true(con['magnification'])
	assert_true(con['x_stage_position'])
	assert_true(con['y_stage_position'])
	assert_true(con['z_stage_position'])
	assert_true(con['comment'])
	assert_true(con['signal'])


def test_parse_condition_003():
	cnd_path = os.path.join(files_dir, 'data003.cnd')
	buffer = open(cnd_path).read()
	con = _parse_condition(buffer)
	assert_equal(con['x_step_number'], 1800)
	assert_equal(con['y_step_number'], 1600)
	assert_equal(con['x_step_size'], 0.5)
	assert_equal(con['y_step_size'], 0.5)
	assert_true(con['magnification'])
	assert_equal(con['x_stage_position'], '16.5407')
	assert_equal(con['y_stage_position'], '19.9220')
	assert_equal(con['z_stage_position'], '11.0355')
	assert_equal(con['comment'], 'ref-mag-kam5')
	assert_equal(con['signal'], 'Ti_CH3_PETH_Ka')
	assert_equal(con['element_name'], 'Ti')
	assert_equal(con['channel_name'], 'CH3')
	assert_equal(con['crystal_name'], 'PETH')
	assert_equal(con['x_ray_name'], 'Ka')
	assert_equal(con['scan_mode'], 'S')


def test_parse_condition_ok10vm_a():
	cnd_path = os.path.join(files_dir, 'OK10VM-a.cnd')
	buffer = open(cnd_path).read()
	con = _parse_condition(buffer)
	assert_equal(con['x_ray_name'], 'Ka')
	#assert_equal(con['comment'], 'OK10VM-a')

def test_parse_condition_ok10vm_a_2():
	cnd_path = os.path.join(files_dir, 'OK10VM-a-2.cnd')
	buffer = open(cnd_path).read()
	con = _parse_condition(buffer)
	assert_equal(con['x_ray_name'], 'Ka')
	assert_equal(con['x_step_number'], 2000)
	assert_equal(con['y_step_number'], 1500)
	assert_equal(con['x_stage_position'], '-19.2155')




def test_parse_condition_006():
	cnd_path = os.path.join(files_dir, 'data006.cnd')
	buffer = open(cnd_path).read()
	con = _parse_condition(buffer)
	assert_equal(con['x_step_number'], 1800)
	assert_equal(con['y_step_number'], 1600)
	assert_true(con['magnification'])
	assert_equal(con['x_stage_position'], '16.5407')
	assert_equal(con['y_stage_position'], '19.9220')
	assert_equal(con['z_stage_position'], '11.0355')
	assert_equal(con['comment'], 'ref-mag-kam5')
	assert_equal(con['signal'], 'COMPO')
#	assert_equal(con['wds_cond_name'], 'Ti_CH3_PETH_Ka')


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


def test_map2info_jpeg_3():
	shutil.copy(os.path.join(files_dir, 'OK10VM-a-2.map'),'tmp')
	shutil.copy(os.path.join(files_dir, 'OK10VM-a-2.cnd'),'tmp')	
	sys.argv = ['map2info', 'tmp/OK10VM-a-2.map']
	map2info()

#@with_setup(setup, teardown)
def test_map2info():
	shutil.copy(os.path.join(files_dir, 'ProbeScan.map'),'tmp')
	shutil.copy(os.path.join(files_dir, 'ProbeScan.cnd'),'tmp')	
	sys.argv = ['map2info', 'tmp/ProbeScan.map']
	map2info()



