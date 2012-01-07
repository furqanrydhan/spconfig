#!/usr/bin/env python

__version_info__ = (0, 1, 4)
__version__ = '.'.join([str(i) for i in __version_info__])
version = __version__

import collections
import ConfigParser
import optparse
import os
import os.path
import sys
import traceback

class clparser(optparse.OptionParser):
    def __init__(self, *args, **kwargs):
        custom_options = {}
        if kwargs.get('options') is not None:
            custom_options = kwargs['options']
            del kwargs['options']
        optparse.OptionParser.__init__(self, *args, **kwargs)
        self.add_option('--root', action='store', type='string', dest='root', help='Specify the directory to search for config files')
        self.add_option('--role', action='store', type='string', dest='role', help='Specify running role, typically one of "prod", "dev", or "local" [default]')
        self.add_option('--config', action='store', type='string', dest='config', help='Use CONFIG instead of any other config files found')
        for option_name in custom_options.keys():
            if custom_options[option_name].get('dest') is not None:
                assert len(custom_options[option_name]['dest'].split('.')) == 2, \
                    "%s must be of the form <section>.<option>" % option_name
                custom_options[option_name]['dest'] = 'custom_options.' + custom_options[option_name]['dest']
            self.add_option(option_name, **custom_options[option_name])
    def error(self, msg):
        print msg + ' (ignoring)'

# Search the directory of the caller's file, or the cwd, or the root directory, for config files.
def configuration(**kwargs):
    defaults = {
        'role': 'local',
    }
    # Find the callstack so we can identify the directory of our caller and use their local config.
    if kwargs.get('root') is None:
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
    # Check if a role was specified, or an explicit config file given.
    parser = clparser(options=kwargs.get('options', {}))
    if 'options' in kwargs:
        del kwargs['options']
    spec.update(kwargs)
    class attrdict(dict):
        def __setattr__(self, key, value):
            return self.__setitem__(key, value)
    (options, args) = parser.parse_args(sys.argv, values=attrdict())
    custom_options = {}
    for key in options.keys():
        if key.startswith('custom_options'):
            custom_options[key.lstrip('custom_options.')] = options[key]
            del options[key]
    if 'custom_options' in options:
        del options['custom_options']
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
    settings = collections.defaultdict(lambda: {})
    parser = ConfigParser.SafeConfigParser()
    parser.read(filenames)
    for section in parser.sections():
        settings[section] = {}
        for option in parser.options(section):
            settings[section][option] = parser.get(section, option)
    for option_name in custom_options.keys():
        (section, option) = option_name.split('.')
        settings[section][option] = custom_options[option_name]
    return settings
    
class configurable(object):
    _settings = {}
    def __init__(self, *args, **kwargs):
        if 'settings' in kwargs:
            self._settings = kwargs['settings']