#!/usr/bin/env python

import ConfigParser
import optparse
import os
import os.path
import sys
import traceback

# Search the directory of the caller's file, or the cwd, or the root directory, for config files.
def configuration(**kwargs):
    defaults = {
        'role': 'local',
    }
    # Find the callstack so we can identify the directory of our caller and use their local config.
    stack = traceback.extract_stack()
    framework_dir = os.path.abspath(os.path.dirname(__file__))
    # Beginning with -2, the caller
    for index in xrange(-2, -1 * (len(stack) + 1), -1):
        caller_dir = os.path.abspath(os.path.dirname(traceback.extract_stack()[index][0]))
        # Exclude our own directory
        if caller_dir != framework_dir:
            defaults['root'] = caller_dir
            break
    if not 'root' in defaults:
        defaults['root'] = os.getcwd()
    spec = dict(defaults)
    spec.update(kwargs)
    # Check if a role was specified, or an explicit config file given.
    parser = optparse.OptionParser()
    parser.add_option('--root', action='store', type='string', dest='root', help='Specify the directory to search for config files')
    parser.add_option('--role', action='store', type='string', dest='role', help='Specify running role, typically one of "prod", "dev", or "local" [default]')
    parser.add_option('--config', action='store', type='string', dest='config', help='Use CONFIG instead of any other config files found')
    class attrdict(dict):
        def __setattr__(self, key, value):
            return self.__setitem__(key, value)
    (options, args) = parser.parse_args(sys.argv, values=attrdict())
    spec.update(options)
    # Compile a list of potential config file names.
    filenames = []
    if 'config' in options:
        filenames.append(spec['config'])
    else:
        filenames.append('default.cfg')
        filenames.append(spec['role'] + '.cfg')
        filenames.append(os.uname()[1] + '.cfg')
    filenames = [os.path.abspath(os.path.join(spec['root'], filename)) for filename in filenames]
    settings = {}
    parser = ConfigParser.SafeConfigParser()
    parser.read(filenames)
    for section in parser.sections():
        settings[section] = {}
        for option in parser.options(section):
            settings[section][option] = parser.get(section, option)
    return settings
    
class configurable(object):
    _settings = {}
    def __init__(self, *args, **kwargs):
        if 'settings' in kwargs:
            self._settings = kwargs['settings']