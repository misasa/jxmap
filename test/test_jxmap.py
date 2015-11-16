import sys
import os
import numpy
import shutil
import re
from nose.tools import *
from jxmap import Jxmap

files_dir = os.path.join(os.path.dirname(__file__), 'files')
saved = None

def setup_tmp():
	if os.path.exists('tmp'):
		shutil.rmtree('tmp')
	os.mkdir('tmp')
	# shutil.copy(os.path.join(files_dir, 'OK10VM-a-2.map'),'tmp')
	# shutil.copy(os.path.join(files_dir, 'OK10VM-a-2.cnd'),'tmp')	
	# shutil.copy(os.path.join(files_dir, 'data006.map'),'tmp')
	# shutil.copy(os.path.join(files_dir, 'data006.cnd'),'tmp')	


def setup():
	setup_tmp()
	global saved
	saved = sys.argv

def teardown():
	sys.argv = saved
	#shutil.rmtree('tmp')

def test_get_dtype():
	assert_equals(Jxmap.get_dtype(2), 'u2')
	assert_equals(Jxmap.get_dtype(4), 'u4')
	assert_equals(Jxmap.get_dtype(8), 'f8')
	assert_raises(RuntimeError, Jxmap.get_dtype, 1)
	assert_raises(RuntimeError, Jxmap.get_dtype, 9)

def test_magnification():
	assert_equal(Jxmap.magnification(240000.0), 0.5)
	assert_equal(Jxmap.magnification(120000.0), 1.0)
	assert_equal(Jxmap.magnification(60000.0), 2.0)

@with_setup(setup, teardown)
def test_read_map_7():
	shutil.copy(os.path.join(files_dir, '7.map'),'tmp')
	imgArray1 = Jxmap.read_map('tmp/7.map', x_step_number = 920, y_step_number =1000, swap_byte = True)
	assert_equals(imgArray1.shape, (1000, 920))
	assert_equals(numpy.amax(imgArray1), 1005)

@with_setup(setup, teardown)
def test_read_map_003():
	shutil.copy(os.path.join(files_dir, 'data003.map'),'tmp')
	imgArray2 = Jxmap.read_map('tmp/data003.map', x_step_number = 1800, y_step_number = 1600)
	assert_equals(imgArray2.shape, (1600, 1800))
	assert_equals(numpy.amax(imgArray2), 67.0)

@with_setup(setup, teardown)
def test_read_map_003_with_instance():
	shutil.copy(os.path.join(files_dir, 'data003.map'),'tmp')
	shutil.copy(os.path.join(files_dir, 'data003.cnd'),'tmp')
	jxmap = Jxmap(map_path = 'tmp/data003.map')
	#imgArray2 = Jxmap.read_map('tmp/data003.map', x_step_number = 1800, y_step_number = 1600)
	jxmap.load_map()
	imgArray2 = jxmap.data
	assert_equals(imgArray2.shape, (1600, 1800))
	assert_equals(numpy.amax(imgArray2), 67.0)

def test_Jxmap_read_cnd0_file():
	buffer = Jxmap.read_cnd0_file(os.path.join(files_dir, '0.cnd'))
	assert_true(re.search(r'Number of measured elements', buffer))	

def test_parse_condition_jxa8530():
	buffer = '''
$SEM_DATA_VERSION 1
$XM_DATA_COUNT_MAX 67.000000
$XM_DATA_COUNT_MIN 0.000000
$XM_DATA_COUNT_AVE 0.423
$XM_DATA_PROBE_CURRENT 1.201e-008
$XM_DATA_PROBE_CURRENT_PRE 1.203e-008
$XM_DATA_PROBE_CURRENT_POST 1.200e-008
$XM_DATA_ACCUM 1
$XM_DATA_SAVE_DATE 2015/03/31 22:46:53
$XM_DATA_FACTOR_A3 0.000000
$XM_DATA_FACTOR_A2 0.000000
$XM_DATA_FACTOR_A 0.000000
$XM_DATA_FACTOR_B 0.000000
$XM_DATA_PROCESSED_DEAD_TIME 0.000000
$XM_DATA_CALC_FACTOR_M 0
$XM_DATA_CALC_FACTOR_N 0
$XM_ANALYSIS_ACQ_OPERATOR User
$XM_ANALYSIS_ACQ_DATE 2015/03/31 22:46:53
$XM_ANALYSIS_HOST_VERSION 1. 10. 0. 4
$XM_ANALYSIS_SERVER_VERSION 1. 10. 0. 2
$XM_ANALYSIS_INSTRUMENT JXA8530
$XM_MAP_ANALYSIS_MODE 0
$XM_AC_EDITABLE 1
$XM_AC_TYPE 5
$XM_CP_EDITABLE 1
$XM_CP_SAVE_PATH C:\EPMA User\ref\mount-magnetites
$XM_CP_PROJECT_NAME 2015-03-31
$XM_CP_DATA_INDEX 1
$XM_CP_DATA_NAME 
$XM_CP_COMMENT REE-rich inclusion
$XM_CP_DATE 2015/03/31 18:03:51
$XM_CP_OPERATOR 
$XM_CP_BASE_RECIPE_NAME 
$XM_CP_ANALYSIS_ALIAS 
$XM_EC_EDITABLE 1
$XM_EC_ACCEL_VOLT 15.0
$XM_EC_TARGET_PROBE_CURRENT 1.20e-008
$XM_EC_AUTO_CURRENT_SWITCH 1
$XM_EC_PROBE_NO 60
$XM_EC_PROBE_FINE 138
$XM_EC_OBJECT_LENS 887702
$XM_EC_WD 11.006
$XM_EC_AFC_SWITCH 0
$XM_EC_ASTG_SWITCH 0
$XM_EC_BST_MODE 0
$XM_EC_ACCEL_VOLT_FLAG 1
$XM_EC_PROBE_CURRENT_FLAG 1
$XM_EC_OBJECT_LENS_FLAG 1
$XM_EC_ASTG_SWITCH_FLAG 0
$XM_EC_BST_MODE_FLAG 0
$XM_VIEW_IMG_NUM_OF_DATA 0
$XM_ELEM_EDITABLE 1
$XM_ELEM_NUMBER_OF_DATA 1
$XM_ELEM_XCLENT 0
$XM_ELEM_TRACE_ANALYSIS_MODE 0
$XM_ELEM_COND_ID%0 0
$XM_ELEM_COND_TYPE%0 0
$XM_ELEM_NAME%0 Ti
$XM_ELEM_SEQ_NO%0 1
$XM_ELEM_CORR_KEY%0 20150331172259446
$XM_ELEM_WDS_COND_NAME%0 Ti_CH3_PETH_Ka
$XM_ELEM_WDS_CHANNEL_NO%0 2
$XM_ELEM_WDS_CRYSTAL_NO%0 0
$XM_ELEM_WDS_CRYSTAL_NAME%0 PETH
$XM_ELEM_WDS_XRAY%0 Ka
$XM_ELEM_WDS_ORDER%0 1
$XM_ELEM_WDS_PEAK%0 87.784
$XM_ELEM_WDS_BACK_MINUS%0 5.000
$XM_ELEM_WDS_BACK_PLUS%0 5.000
$XM_ELEM_WDS_BLANK_FLAG%0 0
$XM_ELEM_WDS_PHA_EDITABLE%0 1
$XM_ELEM_WDS_PHA_HV%0 1618
$XM_ELEM_WDS_PHA_GAIN%0 64
$XM_ELEM_WDS_PHA_MODE%0 Int
$XM_ELEM_WDS_PHA_BASE%0 0.7
$XM_ELEM_WDS_PHA_WINDOW%0 9.3
$XM_ELEM_WDS_PHA_SET_MODE%0 0
$XM_ELEM_WDS_TA_GROUP_ID%0 0
$XM_ELEM_WDS_TA_INTEGRATION%0 0
$XM_ELEM_WDS_TA_CALIBFACTOR_TYPE%0 0
$XM_ELEM_WDS_TA_STD_PATH%0 
$XM_ELEM_WDS_TA_CALIB_FACTOR%0 0.000000 0.000000 0.000000 0.000000
$XM_ELEM_WDS_TA_MATERIAL_TYPE%0 0
$XM_ELEM_WDS_TA_VALENCE%0 0
$XM_AP_TYPE 3
$XM_AP_COMMENT 
$XM_AP_MEASURE_FLAG 1
$XM_AP_NUMBER_OF_DATA 1
$XM_AP_TYPE%0 1
$XM_AP_COMMENT%0 ref-mag-kam5
$XM_AP_MEASURE_FLAG%0 1
$XM_AP_SA_PIXELS%0 1800 1600
$XM_AP_SA_PIXEL_SIZE%0 0.50 0.50 50.00
$XM_AP_SA_DWELL_TIME%0 5.0
$XM_AP_SA_AFC_FLAG%0 0
$XM_AP_SA_ACCUM%0 1
$XM_AP_SA_SCAN_DIRECTION%0 0
$XM_AP_SA_SCAN_MODE%0 1
$XM_AP_SA_PROBE_DIAMETER%0 1
$XM_AP_SA_SCAN_LENGTH%0 1
$XM_AP_SA_ROTATION_ANGLE%0 0.0
$XM_AP_SA_SCAN_SPEED%0 1
$XM_AP_SA_LINE_DIRECTION%0 -1
$XM_AP_SA_BEAM_START_POS%0 0 0
$XM_AP_SA_BEAM_END_POS%0 0 0
$XM_AP_SA_STAGE_POS%0_0 16.5407 19.9220 11.0355
$XM_AP_SA_STAGE_POS%0_1 16.9907 19.5220 11.0355
$XM_AP_SA_STAGE_POS%0_2 16.0907 19.5220 11.0355
$XM_AP_SA_STAGE_POS%0_3 16.0907 20.3220 11.0355
$XM_AP_SA_STAGE_POS%0_4 16.9907 20.3220 11.0355
$XM_AP_SA_MAP_SCAN_AREA_TYPE%0 2
$XM_AP_SA_MAP_EXT_MODE%0 0
$XM_AP_SA_BEAM_BLANK_MODE%0 0
$XM_AP_SA_SHAPE_NUM_OF_DATA%0 0
$XM_AP_SA_SURFACE_NUM_OF_DATA%0 0
$XM_AP_SA_EXTMAP_NUM_OF_LINES%0 0
$XM_EDS_EXEC_MODE 1
$XM_EDS_AUTO_DISP_ELEM_FLAG 1
$XM_EDS_APERTURE_NO 5
$XM_EDS_COUNTING_MODE 2
$XM_EDS_MEASURE_TIME 60
$XM_EDS_MEASURE_MODE 0
$XM_MAP_SS_MAP_ELEM None
$XM_MAP_SS_MAP_SEQ_NO 1
$XM_MAP_SS_MAP_CH_NO 0
'''
	con = Jxmap.parse_condition_jxa8530f(buffer)
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

def test_parse_condition_jxa8530_2():
	buffer = '''
$SEM_DATA_VERSION 1
$XM_DATA_COUNT_MAX 67.000000
$XM_DATA_COUNT_MIN 0.000000
$XM_DATA_COUNT_AVE 0.423
$XM_DATA_PROBE_CURRENT 1.201e-008
$XM_DATA_PROBE_CURRENT_PRE 1.203e-008
$XM_DATA_PROBE_CURRENT_POST 1.200e-008
$XM_DATA_ACCUM 1
$XM_DATA_SAVE_DATE 2015/03/31 22:46:53
$XM_DATA_FACTOR_A3 0.000000
$XM_DATA_FACTOR_A2 0.000000
$XM_DATA_FACTOR_A 0.000000
$XM_DATA_FACTOR_B 0.000000
$XM_DATA_PROCESSED_DEAD_TIME 0.000000
$XM_DATA_CALC_FACTOR_M 0
$XM_DATA_CALC_FACTOR_N 0
$XM_ANALYSIS_ACQ_OPERATOR User
$XM_ANALYSIS_ACQ_DATE 2015/03/31 22:46:53
$XM_ANALYSIS_HOST_VERSION 1. 10. 0. 4
$XM_ANALYSIS_SERVER_VERSION 1. 10. 0. 2
$XM_ANALYSIS_INSTRUMENT JXA8530
$XM_MAP_ANALYSIS_MODE 0
$XM_AC_EDITABLE 1
$XM_AC_TYPE 5
$XM_CP_EDITABLE 1
$XM_CP_SAVE_PATH C:\EPMA User\ref\mount-magnetites
$XM_CP_PROJECT_NAME 2015-03-31
$XM_CP_DATA_INDEX 1
$XM_CP_DATA_NAME 
$XM_CP_COMMENT REE-rich inclusion
$XM_CP_DATE 2015/03/31 18:03:51
$XM_CP_OPERATOR 
$XM_CP_BASE_RECIPE_NAME 
$XM_CP_ANALYSIS_ALIAS 
$XM_EC_EDITABLE 1
$XM_EC_ACCEL_VOLT 15.0
$XM_EC_TARGET_PROBE_CURRENT 1.20e-008
$XM_EC_AUTO_CURRENT_SWITCH 1
$XM_EC_PROBE_NO 60
$XM_EC_PROBE_FINE 138
$XM_EC_OBJECT_LENS 887702
$XM_EC_WD 11.006
$XM_EC_AFC_SWITCH 0
$XM_EC_ASTG_SWITCH 0
$XM_EC_BST_MODE 0
$XM_EC_ACCEL_VOLT_FLAG 1
$XM_EC_PROBE_CURRENT_FLAG 1
$XM_EC_OBJECT_LENS_FLAG 1
$XM_EC_ASTG_SWITCH_FLAG 0
$XM_EC_BST_MODE_FLAG 0
$XM_VIEW_IMG_NUM_OF_DATA 0
$XM_ELEM_EDITABLE 1
$XM_ELEM_NUMBER_OF_DATA 1
$XM_ELEM_XCLENT 0
$XM_ELEM_TRACE_ANALYSIS_MODE 0
$XM_ELEM_COND_ID%0 0
$XM_ELEM_COND_TYPE%0 0
$XM_ELEM_NAME%0 Ti
$XM_ELEM_SEQ_NO%0 1
$XM_ELEM_CORR_KEY%0 20150331172259446
$XM_ELEM_WDS_COND_NAME%0 P_ch2_TAPL
$XM_ELEM_WDS_CHANNEL_NO%0 2
$XM_ELEM_WDS_CRYSTAL_NO%0 0
$XM_ELEM_WDS_CRYSTAL_NAME%0 TAPL
$XM_ELEM_WDS_XRAY%0 Ka
$XM_ELEM_WDS_ORDER%0 1
$XM_ELEM_WDS_PEAK%0 87.784
$XM_ELEM_WDS_BACK_MINUS%0 5.000
$XM_ELEM_WDS_BACK_PLUS%0 5.000
$XM_ELEM_WDS_BLANK_FLAG%0 0
$XM_ELEM_WDS_PHA_EDITABLE%0 1
$XM_ELEM_WDS_PHA_HV%0 1618
$XM_ELEM_WDS_PHA_GAIN%0 64
$XM_ELEM_WDS_PHA_MODE%0 Int
$XM_ELEM_WDS_PHA_BASE%0 0.7
$XM_ELEM_WDS_PHA_WINDOW%0 9.3
$XM_ELEM_WDS_PHA_SET_MODE%0 0
$XM_ELEM_WDS_TA_GROUP_ID%0 0
$XM_ELEM_WDS_TA_INTEGRATION%0 0
$XM_ELEM_WDS_TA_CALIBFACTOR_TYPE%0 0
$XM_ELEM_WDS_TA_STD_PATH%0 
$XM_ELEM_WDS_TA_CALIB_FACTOR%0 0.000000 0.000000 0.000000 0.000000
$XM_ELEM_WDS_TA_MATERIAL_TYPE%0 0
$XM_ELEM_WDS_TA_VALENCE%0 0
$XM_AP_TYPE 3
$XM_AP_COMMENT 
$XM_AP_MEASURE_FLAG 1
$XM_AP_NUMBER_OF_DATA 1
$XM_AP_TYPE%0 1
$XM_AP_COMMENT%0 ref-mag-kam5
$XM_AP_MEASURE_FLAG%0 1
$XM_AP_SA_PIXELS%0 1800 1600
$XM_AP_SA_PIXEL_SIZE%0 0.50 0.50 50.00
$XM_AP_SA_DWELL_TIME%0 5.0
$XM_AP_SA_AFC_FLAG%0 0
$XM_AP_SA_ACCUM%0 1
$XM_AP_SA_SCAN_DIRECTION%0 0
$XM_AP_SA_SCAN_MODE%0 1
$XM_AP_SA_PROBE_DIAMETER%0 1
$XM_AP_SA_SCAN_LENGTH%0 1
$XM_AP_SA_ROTATION_ANGLE%0 0.0
$XM_AP_SA_SCAN_SPEED%0 1
$XM_AP_SA_LINE_DIRECTION%0 -1
$XM_AP_SA_BEAM_START_POS%0 0 0
$XM_AP_SA_BEAM_END_POS%0 0 0
$XM_AP_SA_STAGE_POS%0_0 16.5407 19.9220 11.0355
$XM_AP_SA_STAGE_POS%0_1 16.9907 19.5220 11.0355
$XM_AP_SA_STAGE_POS%0_2 16.0907 19.5220 11.0355
$XM_AP_SA_STAGE_POS%0_3 16.0907 20.3220 11.0355
$XM_AP_SA_STAGE_POS%0_4 16.9907 20.3220 11.0355
$XM_AP_SA_MAP_SCAN_AREA_TYPE%0 2
$XM_AP_SA_MAP_EXT_MODE%0 0
$XM_AP_SA_BEAM_BLANK_MODE%0 0
$XM_AP_SA_SHAPE_NUM_OF_DATA%0 0
$XM_AP_SA_SURFACE_NUM_OF_DATA%0 0
$XM_AP_SA_EXTMAP_NUM_OF_LINES%0 0
$XM_EDS_EXEC_MODE 1
$XM_EDS_AUTO_DISP_ELEM_FLAG 1
$XM_EDS_APERTURE_NO 5
$XM_EDS_COUNTING_MODE 2
$XM_EDS_MEASURE_TIME 60
$XM_EDS_MEASURE_MODE 0
$XM_MAP_SS_MAP_ELEM None
$XM_MAP_SS_MAP_SEQ_NO 1
$XM_MAP_SS_MAP_CH_NO 0
'''
	con = Jxmap.parse_condition_jxa8530f(buffer)
	assert_equal(con['x_step_number'], 1800)
	assert_equal(con['y_step_number'], 1600)
	assert_equal(con['x_step_size'], 0.5)
	assert_equal(con['y_step_size'], 0.5)
	assert_true(con['magnification'])
	assert_equal(con['x_stage_position'], '16.5407')
	assert_equal(con['y_stage_position'], '19.9220')
	assert_equal(con['z_stage_position'], '11.0355')
	assert_equal(con['comment'], 'ref-mag-kam5')
	assert_equal(con['signal'], 'P_ch2_TAPL')
	assert_equal(con['element_name'], 'P')
	assert_equal(con['channel_name'], 'ch2')
	assert_equal(con['crystal_name'], 'TAPL')
	assert_equal(con['x_ray_name'], 'Ka')
	assert_equal(con['scan_mode'], 'S')


def test_parse_condition_jxa8800():
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
	con = Jxmap.parse_condition_jxa8800(buffer)
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

def test_with_map_path_data006():
	jxmap = Jxmap(map_path=os.path.join(files_dir, 'data006.map'))
	assert_equal(jxmap.cnd_path, os.path.join(files_dir, 'data006.cnd'))
	assert_true(jxmap.condition['x_step_number'])

def test_with_map_path_7():
	jxmap = Jxmap(map_path=os.path.join(files_dir, '7.map'))
	assert_equal(jxmap.cnd_path, os.path.join(files_dir, '0.cnd'))
	assert_true(jxmap.condition['x_step_number'])

def test_init_with_condition():
	stage_position = (16.5407, 19.9220)
	step_number = (1800, 1600)
	step_size = (0.5, 0.5)
	jxmap = Jxmap(condition={'magnification': 2.3})
	assert_equal(jxmap.condition.get('magnification'), 2.3)
	# assert_equal(jxmap.center, stage_position)
	# assert_equal(jxmap.step_number, step_number)
	# assert_equal(jxmap.step_size, step_size)
	# assert_equal(jxmap.size[0], step_size[0] * step_number[0])


def test_with_sem_info():
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
	condition = Jxmap.parse_condition(buffer)
	jxmap = Jxmap(condition = condition)
	text = jxmap.sem_info()
	assert_true(re.search(r'\$CM_TITLE Hello World F_CH1_TAP_Ka', text))	
	assert_true(re.search(r'\$CM_MAG (\d+)', text))
	assert_true(re.search(r'\$CM_FULL_SIZE 920 1000', text))		
	assert_true(re.search(r'\$CM_STAGE_POS -20\.8380 16\.8980 10\.7432 0 0 0', text))
	assert_true(re.search(r'\$\$SM_SCAN_ROTATION 0\.00', text))

