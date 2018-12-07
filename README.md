# python package -- jxmap

Convert a map file created by JEOL's EPMA to a tiff file.

Datasets of area analyses using JEOL's EPMA are stored in file with extention '.map'.
A program by this package reads '.map' file and writes '.tiff' file.
Also, a program by this package identifies phases using algorithm k-mean.

See [rails project -- epma_archiver](http://gitlab.misasa.okayama-u.ac.jp/rails/epma_archiver)
that refers to this package.
See [rails project -- jxa](http://gitlab.misasa.okayama-u.ac.jp/rails/jxa)
that refers to this package.

This project took over rake project -- jxa1 from 2012-12.

# Dependency

## [Python 2.7 for Windows](https://www.python.org/downloads/windows/)

Include "C:\Python27\;C:\Python27\Scripts\" to %PATH%.

## [matplotlib](http://matplotlib.org/ "When your computer is without development environment, download and launch installer.")

## [scipy](http://sourceforge.net/projects/scipy/ "When your computer is without development environment, download and launch installer.")

# Installation

Install it as Administrator as:

    ADMIN.CMD> pip install git+http://gitlab.misasa.okayama-u.ac.jp/pythonpackage/jxmap.git

Or download [archive.zip](http://gitlab.misasa.okayama-u.ac.jp/pythonpackage/jxmap/repository/archive.zip) to a local directory and install it as Administrator as:

    $ cd ~/Downloads/
    $ wget http://gitlab.misasa.okayama-u.ac.jp/pythonpackage/jxmap/repository/archive.zip
    ADMIN.CMD> cd %USERPROFILE%\Downloads
    ADMIN.CMD> pip list
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
