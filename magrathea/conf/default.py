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

# Default character set to be used for any byte sequence or
# string conversion operations
DEFAULT_CHARSET = 'utf-8'


# LOGGING
#########

# Default log type
DEFAULT_LOG_TYPE = 'term'

# Default log level
DEFAULT_LOG_LEVEL = 'notice'

# Default log file
DEFAULT_LOG_FILE = '/var/log/magrathea.log'

# Default syslog facility
DEFAULT_LOG_FACILITY = 'LOG_USER'

# Default timestamp format for file logging
DEFAULT_LOG_TIMESTAMP = '%Y-%m-%d %H:%M:%S'

# By default, use colors for logging where available
DEFAULT_LOG_COLOR = True
