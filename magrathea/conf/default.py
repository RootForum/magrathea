# -*- coding: utf-8 -*-
"""
    magrathea.conf.default
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""

# This file contains all default settings used anywhere in the Magrathea code.
# As a matter of principle, all settings can be overridden (where it makes
# sense).
#
# Please note:
# As a convention, all default setting designators have to be typed
# in capital letters.


# CORE Settings
###############

#: Default character set to be used for any byte sequence or string conversion operations
DEFAULT_CHARSET = 'utf-8'


# LOGGING
#########

#: Default log type
DEFAULT_LOG_TYPE = 'term'

#: Default log level
DEFAULT_LOG_LEVEL = 'notice'

#: Default log file
DEFAULT_LOG_FILE = '/var/log/magrathea.log'

#: Default syslog facility
DEFAULT_LOG_FACILITY = 'LOG_USER'

#: Default timestamp format for file logging
DEFAULT_LOG_TIMESTAMP = '%Y-%m-%d %H:%M:%S'

#: By default, use colors for logging where available
DEFAULT_LOG_COLOR = True


# PLANET STRUCTURE
##################

#: Default theme directory
DEFAULT_PLANET_THEME_DIR = 'themes'

#: Default build directory
DEFAULT_PLANET_BUILD_DIR = 'build'

#: Default planet configuration file
DEFAULT_PLANET_CONF_FILE = 'planet.ini'

#: Default planet cache file (indicated without suffix)
DEFAULT_PLANET_CACHE_FILE = 'cache'


# PLANET CONFIGURATION
######################

#: Default planet configuration theme key
DEFAULT_PLANET_CONF_THEME_KEY = 'theme'

#: Default planet configuration theme value
DEFAULT_PLANET_CONF_THEME_VAL = 'default'

#: Default planet configuration policy key
DEFAULT_PLANET_CONF_POLICY_KEY = 'policy'

#: Default planet configuration policy global value
DEFAULT_PLANET_CONF_POLICY_VAL_GLOBAL = 'global'

#: Default planet configuration policy local value
DEFAULT_PLANET_CONF_POLICY_VAL_LOCAL = 'local'

#: Default planet configuration policy hours value
DEFAULT_PLANET_CONF_POLICY_VAL_HOURS = 'hours'

#: Default planet configuration policy days value
DEFAULT_PLANET_CONF_POLICY_VAL_DAYS = 'days'

#: Default planet configuration policy weeks value
DEFAULT_PLANET_CONF_POLICY_VAL_WEEKS = 'weeks'

#: Default planet configuration policy months value
DEFAULT_PLANET_CONF_POLICY_VAL_MONTHS = 'months'

#: Default planet configuration policy none value
DEFAULT_PLANET_CONF_POLICY_VAL_NONE = 'none'

#: Default planet configuration policy value
DEFAULT_PLANET_CONF_POLICY_VAL = DEFAULT_PLANET_CONF_POLICY_VAL_DAYS

#: Default planet configuration limit key
DEFAULT_PLANET_CONF_LIMIT_KEY = 'limit'

#: Default planet configuration limit value
DEFAULT_PLANET_CONF_LIMIT_VAL = 5

#: Default planet configuration paginate key
DEFAULT_PLANET_CONF_PAGINATE_KEY = 'paginate'

#: Default planet configuration paginate value
DEFAULT_PLANET_CONF_PAGINATE_VAL = 25

#: Default planet configuration theme directory key
DEFAULT_PLANET_CONF_THEME_DIR_KEY = 'theme_dir'

#: Default planet configuration theme directory value
DEFAULT_PLANET_CONF_THEME_DIR_VAL = DEFAULT_PLANET_THEME_DIR

#: Default planet configuration build directory key
DEFAULT_PLANET_CONF_BUILD_DIR_KEY = 'build_dir'

#: Default planet configuration build directory value
DEFAULT_PLANET_CONF_BUILD_DIR_VAL = DEFAULT_PLANET_BUILD_DIR

#: Default planet configuration cache file key
DEFAULT_PLANET_CONF_CACHE_FILE_KEY = 'cache_file'

#: Default planet configuration cache file value (without suffix)
DEFAULT_PLANET_CONF_CACHE_FILE_VAL = DEFAULT_PLANET_CACHE_FILE

#: Default planet configuration per feed author key
DEFAULT_PLANET_CONF_FEED_AUTHOR_KEY = 'author'

#: Default planet configuration per feed author value
DEFAULT_PLANET_CONF_FEED_AUTHOR_VAL = ''

#: Default planet configuration per feed title key
DEFAULT_PLANET_CONF_FEED_TITLE_KEY = 'title'

#: Default planet configuration per feed title value
DEFAULT_PLANET_CONF_FEED_TITLE_VAL = ''
