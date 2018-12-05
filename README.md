# python package -- jxmap

Convert a map file created by JEOL's EPMA to a tiff file.

Map files created by JEOL's EPMA are with extention '.map'.  This package also offers
a program that identifies phases using an algorithm k-mean.

See [rails project -- epma_archiver](http://gitlab.misasa.okayama-u.ac.jp/rails/epma_archiver)
and
[rails project -- jxa](http://gitlab.misasa.okayama-u.ac.jp/rails/jxa).

See
[EMPA-archiver for JXA-8530F](http://gitlab.misasa.okayama-u.ac.jp/rails/epma_archiver)
and
[EMPA-archiver for JXA-8800](http://gitlab.misasa.okayama-u.ac.jp/rails/jxa)
that refer to this package.

# Dependency

## [Python 2.7 for Windows](https://www.python.org/downloads/windows/)

Include "C:\Python27\;C:\Python27\Scripts\" to %PATH%.

## [matplotlib](http://matplotlib.org/ "download and launch installer")

## [scipy](http://sourceforge.net/projects/scipy/ "download and launch installer")

# Installation

Install it as Administrator as:

    ADMIN.CMD> pip install git+http://gitlab.misasa.okayama-u.ac.jp/pythonpackage/jxmap.git

Or download [archive.zip](http://gitlab.misasa.okayama-u.ac.jp/pythonpackage/jxmap/repository/archive.zip) to a local directory and install it as Administrator as:

    ADMIN.CMD> pip list
    $ wget http://gitlab.misasa.okayama-u.ac.jp/pythonpackage/jxmap/repository/archive.zip
    ADMIN.CMD> pip install archive.zip

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
