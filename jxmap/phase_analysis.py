#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import numpy
import pickle
#sys.path.insert(0, os.path.dirname( os.path.abspath( __file__ ) ) + "/../lib")
#import mylib

from PIL import Image
from pylab import *

from scipy.cluster.vq import *
from scipy.misc import imresize
from optparse import OptionParser
from jxmap import load_rpl, load_raw, load_pickle

def map_create():
	# parser = OptionParser("usage: %prog [options] name")
	parser = OptionParser("""usage: %prog [options] phasefile
	SYNOPSIS AND USAGE
	  python %prog [options] phasefile

	DESCRIPTION
	  Convert a phasefile to N-phase pseudocolor-map.  By phases analysis
	  using `phase-analysis-kmeans.py', you obtain phasefile
	  `phases-N.pkl'.  This program generates N-phase pseudocolor-map
	  *.raw accompanied with *.rpl and *.lisp to be loaded into LISPIX to
	  have a visual.

	EXAMPLE
	  DOS> python %prog phase-8.pkl
	  DOS> dir
	  ...
	  phases-8.lisp
	  phases-8.raw
	  phases-8.rpl
	  ...

	SEE ALSO
	  phase-analysis-kmeans.py
	  LISPIX <http://www.nist.gov/lispix>
	  http://dream.misasa.okayama-u.ac.jp

	IMPLEMENTATION
	  Orochi, version 9
	  Copyright (C) 2014 Okayama University
	  License GPLv3+: GNU GPL version 3 or later

	HISTORY
	  May 24, 2015: TK add documentation
	""")
	parser.add_option("-v", "--verbose",
	                  action="store_true", dest="verbose", default=False,
	                  help="make lots of noise")

	(options, args) = parser.parse_args()
	if len(args) < 1:
	    parser.error("incorrect number of arguments")

	name = args[0]
	#colors = ["Red", "Green", "Blue", "Yellow", "Magenta", "Cyan", "Light Orange", "Light Green", "Dark Green", "Light Blue", "Light Brown", "Light Pastel Blue", "Violet", "Tan", "Sky Blue"]

	root_name, ext = os.path.splitext(name)
	basename = os.path.basename(root_name)
	dirname = os.path.dirname(root_name)
	pkl_path = os.path.join(dirname, basename + '.pkl')
	default_lisp_path = os.path.join(dirname, basename + '.lisp')
	default_raw_path = os.path.join(dirname, basename + '.raw')
	default_rpl_path = os.path.join(dirname, basename + '.rpl')
	default_image_path = os.path.join(dirname, basename + '.tiff')
	pm = load_pickle(pkl_path)
	pm.load_features()
	pm.show_table(sys.stdout)
	pm.dump_raw(default_raw_path)
	pm.dump_image(default_image_path)
	pm.dump_rpl(default_rpl_path)
	pm.dump_lisp(default_lisp_path, root_name)
	if False:
		colors = []
		for color in pm.plot_colors:
			rgb = matplotlib.colors.ColorConverter().to_rgb(color)
			colors.append([int(f * 255) for f in rgb])
			
		codeim = pm.code.reshape(pm.height,pm.width)
		yPix, xPix = codeim.shape
		data = numpy.zeros( (yPix,xPix,3), dtype=numpy.uint8)
		for i in range(len(pm.table)):
			data[numpy.where(codeim == i)] = colors[i]

		img = Image.fromarray(data, 'RGB')
		img.save(default_image_path)
	#sys.exit()

def phase_analysis_kmeans():
	# parser = OptionParser("usage: %prog [options] image ...")
	parser = OptionParser("""usage: %prog [options] map0 map1 map2 [... mapM]
	SYNOPSIS AND USAGE
	  python %prog [options] image0 image1 image2 [... imageM]

	DESCRIPTION
	  Create phasefile with N phases using M input element-maps.  Prepare
	  M input element-maps, that are *.raw accompanied with *.rpl.  This
	  program creates a phasefile with N phases `pnases-N.pkl'.  Call
	  `phase-map-creation.py' subsequently to have N-phase pseudocolor-map
	  *.raw and *.rpl.

	EXAMPLE
	  DOS> python %prog -n 8 Al.raw CP.raw Ca.raw Cl.raw Cr.raw Fe.raw Mg.raw Mn.raw Na.raw Ni.raw Si.raw Ti.raw
	  DOS> dir
	  ...
	  phases-8.pkl
	  ...

	SEE ALSO
	  phase-map-creation.py
	  http://dream.misasa.okayama-u.ac.jp

	IMPLEMENTATION
	  Orochi, version 9
	  Copyright (C) 2014 Okayama University
	  License GPLv3+: GNU GPL version 3 or later

	HISTORY
	  May 24, 2015: TK add documentation
	""")
	parser.add_option("-v", "--verbose",
	                  action="store_true", dest="verbose", default=False,
	                  help="make lots of noise")
	parser.add_option("-n", "--num_phases",
	                  type = int, dest="num_phase", default=5,
	                  help="specify number of phases")

	(options, args) = parser.parse_args()
	if len(args) < 1:
	    parser.error("incorrect number of arguments")

	src1_path = args[0]
	imlist = []
	basenames = []
	for arg in args:
		root, ext = os.path.splitext(arg)
		basenames.append(os.path.basename(root))	
		imlist.append(arg)
		
	element_names = [ os.path.splitext(imname)[0] for imname in imlist ]

	raw_path = imlist[0]
	root, ext = os.path.splitext(raw_path)
	dirname = os.path.dirname(raw_path)
	rpl_path = os.path.join(dirname, os.path.basename(root) + '.rpl')
	rpl = load_rpl(rpl_path)

	#print rpl.byteorder

	width = int(rpl['width'])
	height = int(rpl['height'])

	# pickle_name = '-'.join(basenames) + '-' + str(options.num_phase) + 'phase'
	pickle_name = 'phases-' + str(options.num_phase) # by TK on November 6 (2013)
	pickle_path = os.path.join(dirname, pickle_name + '.pkl')
	f_pickle = open(pickle_path, 'wb')
	pickle.dump(imlist,f_pickle)
	pickle.dump(options.num_phase,f_pickle)
	#sys.exit()

	m = height
	n = width
	imnbr = len(imlist) # 画像数の得る


	ims = []
	for path in imlist:
		rpl_path = os.path.join(dirname, os.path.basename(root) + '.rpl')
		tmp_rpl = load_rpl(rpl_path)
	#	ims = numpy.append(ims, numpy.fromfile(path, dtype='<u2',count=int(width)*int(height)))
		ims = numpy.append(ims, load_raw(path, tmp_rpl))	

	features = ims.reshape(imnbr, int(width)*int(height)).transpose()	

	# クラスタリング
	centroids,variance = kmeans(features,options.num_phase)
	code,distance = vq(features,centroids)

	pickle.dump(centroids,f_pickle)
	pickle.dump(variance,f_pickle)
	pickle.dump(code,f_pickle)
	pickle.dump(distance,f_pickle)


	pixel_counts = []
	intensity_ranges = []
	for idx in range(len(centroids)):
		locs = numpy.where(code == idx)[0]
		pixel_counts.append(len(locs))
		t = []
		for element_idx in range(len(element_names)): 
			fs = features[locs, element_idx]
			t.append( [ numpy.min(fs), numpy.max(fs) ] )
		intensity_ranges.append(t)

	pixel_sum = sum(pixel_counts)
	pixel_percents = [  pix/float(pixel_sum) * 100 for pix in pixel_counts ]
	print "%5s" % "index" + "%10s" % "area%" + ''.join( [ "%10s (%5s - %5s)" % (element, "min", "max") for element in element_names] )
	for idx in range(len(centroids)):
		centroid = centroids[idx]
		intensity_range = intensity_ranges[idx]
		line = "%5d" % idx + "%10.2f" % pixel_percents[idx]
		for element_idx in range(len(element_names)):
			mean = centroid[element_idx]
			line += "%10.2f" % mean
			line += " (%5d - %5d)" % (intensity_range[element_idx][0], int(intensity_range[element_idx][1]))
		print line

	# クラスタのラベルを使って画像を生成する
	#print code.shape
	#print distance.shape
	#print code
	#print distance
	#codeim = code.reshape(m,n)
	#print codeim
	#codeim = imresize(codeim,im.shape[:2],interp='nearest')
	if False:
		figure()
		axis('off')
		imshow(codeim)
		show()
