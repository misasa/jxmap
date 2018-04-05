# jxmap

Convert a map file created by JEOL's EPMA to a tiff file.  This package is called from EMPA achievers as listed as below.

## [EMPA-archiver for JXA-8530F](http://devel.misasa.okayama-u.ac.jp/gitlab/rails/epma_archiver)
## [EMPA-archiver for JXA-8800](http://devel.misasa.okayama-u.ac.jp/gitlab/rails/jxa)

# Dependency

## [python 2.7](https://www.python.org/downloads/)

When install Python for MS Windows, do not forget to include `C:\Python27\;C:\Python27\Scripts\` in %PATH%.

## [pip](https://pip.pypa.io/en/latest/installing.html "download and DOS> python get-pip.py")

## [numpy](http://sourceforge.net/projects/numpy/files/NumPy/ "download and launch installer")

## [scipy](http://sourceforge.net/projects/scipy/ "download and launch installer")

## [pil](http://www.pythonware.com/products/pil/ "download and launch installer")

## [matplotlib](http://matplotlib.org/ "download and launch installer")

## [six](http://www.misasa.okayama-u.ac.jp "DOS> pip install six")

## [dateutil](http://www.misasa.okayama-u.ac.jp "DOS> pip install python-dateutil")

## [pyparsing](http://www.misasa.okayama-u.ac.jp "DOS> pip install pyparsing")


# Installation

Install it as Administrator as:

    ADMIN.CMD> pip install git+http://devel.misasa.okayama-u.ac.jp/gitlab/pythonpackage/jxmap.git

Or download [jxmap-xxxyyyzzz.zip](http://devel.misasa.okayama-u.ac.jp/gitlab/pythonpackage/jxmap/repository/archive.zip) to local directory and install it as Administrator as:

    ADMIN.CMD> pip install jxmap-c18fb69e5c558269b4c0285d77b9b12708f37424.zip

Successful installation is confirmed by:

    CMD> jxmap-info --help

# Commands

Commands are summarized as:

| command               | description                                                 | note |
| --------------------- | ----------------------------------------------------------- | ---- |
| jxmap-image           | No description available                                    |      |
| jxmap-info            | Read pseudo imajeoletry and export to imageometry to stdout |      |
| phase-analysis-kmeans | Create phasefile with N phases using M input element-maps   |      |
| phase-map-creation    | Convert a phasefile to N-phase pseudocolor-map              |      |
| u8raw                 | Reduce size of mapfile                                      |      |


# Usage

See online document with option `--help`.
