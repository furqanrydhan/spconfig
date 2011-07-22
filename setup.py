#!/usr/bin/env python
# -*- coding: utf-8 -*-

import distutils.core
 
def setup():
    distutils.core.setup(
        name='stylepage-config',
        version='0.1',
        description='StylePage tools: Python configuration',
        author='mattbornski',
        url='http://github.com/mattbornski/spconfig',
        package_dir={'': 'src'},
        py_modules=[
            'spconfig',
        ],
    )

if __name__ == '__main__':
    setup()