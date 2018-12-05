from setuptools import setup, find_packages
import sys, os

from jxmap import __version__ as VERSION

setup(name='jxmap',
      version=VERSION,
      description="JEOL X-ray Map",
      long_description="""\
JEOL X-ray Map""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='image',
      author='Yusuke Yachi',
      author_email='yyachi@misasa.okayama-u.ac.jp',
      url='http://dream.misasa.okayama-u.ac.jp',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['Nose'],
      #pip install numpy python-dateutil pytz pyparsing six --force-reinstall --upgrade
      install_requires=[
          # -*- Extra requirements: -*-
            "PyYAML",
            "PIL",
            "numpy",
            "python-dateutil",
            "pytz", 
            "pyparsing", 
            "six",
            "scipy",
            "dateutil",
            "matplotlib",
      ],
      entry_points= {
            "console_scripts": [
                  "jxmap-image = jxmap.map2image:map2image",
                  "jxmap-info = jxmap.map2info:map2info",
                  "u8raw = jxmap.u8raw:u8raw",
                  "phase-analysis-kmeans = jxmap.phase_analysis:phase_analysis_kmeans",
                  "phase-map-creation = jxmap.phase_analysis:map_create",                  
                  #"jxmap-raw = jxmap.commands:map2raw",
                  ]},
      )
