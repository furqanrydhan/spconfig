#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import setuptools
 
def setup():
    with open(os.path.join('src', '_version.py'), 'r') as f:
        for line in f.readlines():
            if 'version' in line:
                try:
                    exec(line)
                except SyntaxError:
                    pass
    try:
        assert(isinstance(version, basestring))
    except AssertionError:
        version = 'unknown'
        
    setuptools.setup(
        name='spconfig',
        version=version,
        description='StylePage tools: Python configuration',
        author='mattbornski',
        url='http://github.com/stylepage/spconfig',
        package_dir={'': 'src'},
        py_modules=[
            'spconfig',
        ],
    )

if __name__ == '__main__':
    setup()