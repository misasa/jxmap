# jxmap

Analyze mapfile craeted by EPMA

# Dependency

## [pip](https://pip.pypa.io/en/latest/installing.html "download and DOS> python get-pip.py")

## [numpy](http://sourceforge.net/projects/numpy/files/NumPy/ "download and launch installer")

## [scipy](http://sourceforge.net/projects/scipy/ "download and launch installer")

## [pil](http://www.pythonware.com/products/pil/ "download and launch installer")

## [matplotlib](http://matplotlib.org/ "download and launch installer")

## [six](http://www.misasa.okayama-u.ac.jp "DOS> pip install six")

## [dateutil](http://www.misasa.okayama-u.ac.jp "DOS> pip install python-dateutil")

## [pyparsing](http://www.misasa.okayama-u.ac.jp "DOS> pip install pyparsing")


# Installation

Install it as Administrator by yourself as:

    DOS> pip install git+http://devel.misasa.okayama-u.ac.jp/gitlab/pythonpackage/jxmap.git

Successful installation is confirmed by:

    DOS> jxmap-info -h

# Commands

Commands are summarized as:

| command        | description                                    | note |
| -------------- | ---------------------------------------------- | ---- |
| phase_analysis | Convert a phasefile to N-phase pseudocolor-map |      |
| u8raw          | Reduce size of mapfile                         |      |
| jxmap-info     | Provide info for mapfile                       |      |


# Usage

See online document:

    DOS> phase_analysis --help
    DOS> u8raw --help
    DOS> jxmap-info --help