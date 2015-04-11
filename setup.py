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
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points= {
            "console_scripts": [
                  "jxmap-image = jxmap.commands:map2image",
                  #"jxmap-raw = jxmap.commands:map2raw",
                  ]},
      )
