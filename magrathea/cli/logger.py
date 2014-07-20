# -*- coding: utf-8 -*-
"""
    magrathea.cli.logger
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the RootForum.org team, see AUTHORS.
    :license: MIT License, see LICENSE for details.
"""
import time
import sys
import syslog
from datetime import datetime
from ..conf import get_conf
from ..utils.singleton import Singleton
from ..utils import termcolor


Levels = {
    'mute': (0, '', ''),
    'error': (1, 'ERROR', 'LOG_ERR'),
    'warning': (2, 'WARN ', 'LOG_WARNING'),
    'notice': (3, 'NOTE ', 'LOG_NOTICE'),
    'info': (4, 'INFO ', 'LOG_INFO'),
    'debug': (5, 'DEBUG', 'LOG_DEBUG')
}


@Singleton
class Logger(object):
    """
    Class providing the output interface

    :param str type:     Type of this logger. Must be one of `file`, `syslog` or `term`.
    :param str level:    Minimum level for logging. Must be one of `mute`, `error`, `warning`, `info` or `debug`.
    :param str file:     Path of the log file to log into if type is set to `file`.
    :param str facility: Name of the syslog facility to log into if type is set to `syslog`
    :param bool color:   Allow colored logging (only effective if type is set to `term`)
    """

    def __init__(self, *args, **kwargs):
        self._levels = Levels
        self._level = get_conf('DEFAULT_LOG_LEVEL')
        self._type = get_conf('DEFAULT_LOG_TYPE')
        self._logfile = get_conf('DEFAULT_LOG_FILE')
        self._facility = get_conf('DEFAULT_LOG_FACILITY')
        self._queue = {
            'std': {},
            'err': {}
        }
        self._fp_std = None
        self._fp_err = None

        color_candidate = get_conf('DEFAULT_LOG_COLOR')

        # Check for positional arguments
        if len(args) > 0 and args[0] in ('file', 'term', 'syslog'):
            self._type = args[0]
        if len(args) > 1 and args[1] in self._levels:
            self._level = args[1]
        if len(args) > 2 and type(args[2]) == str:
            self._logfile = args[2]
        if len(args) > 3 and hasattr(syslog, args[3]):
            self._facility = args[3]
        if len(args) > 4 and type(args[4]) == bool:
            color_candidate = args[4]

        # Check for keyword arguments
        if 'type' in kwargs and kwargs['type'] in ('file', 'term', 'syslog'):
            self._type = kwargs['type']
        if 'level' in kwargs and kwargs['level'] in self._levels:
            self._level = kwargs['level']
        if 'file' in kwargs:
            self._logfile = kwargs['file']
        if 'facility' in kwargs and hasattr(syslog, kwargs['facility']):
            self._facility = kwargs['facility']
        if 'color' in kwargs and type(kwargs['color']) == bool:
            color_candidate = kwargs['color']

        # finally decide about color support and open the log channel
        if termcolor.supports_color() and self._type == 'term':
            self._color = color_candidate
        else:
            self._color = False
        self._open()

    def _open(self):
        """Open the log channel"""
        if self._type == 'term':
            self._fp_std = sys.stdout
            self._fp_err = sys.stderr
        elif self._type == 'file':
            # enforce lazy behaviour
            self._fp_std = None
            self._fp_err = None
        elif self._type == 'syslog':
            syslog.openlog(facility=getattr(syslog, self._facility))

    def _close(self):
        """Close the current log channel"""
        if self._type == 'term':
            self._fp_std = None
            self._fp_err = None
        elif self._type == 'file':
            self._fp_std.close()
            self._fp_err = None
        elif self._type == 'syslog':
            syslog.closelog()

    def _flush(self):
        """Flush log queue to the log channel"""
        if self._type == 'term':
            self._flush_term()
        elif self._type == 'file':
            self._flush_file()

    def _flush_term(self):
        """Flush implementation for terminal logging"""
        self._flush_term_err(self._queue['err'])
        self._flush_term_std(self._queue['std'])

    def _flush_term_std(self, queue):
        """Flushes the stdout message queue on a terminal"""
        for msg in sorted(queue.keys()):
            print(queue[msg][1], file=self._fp_std)

    def _flush_term_err(self, queue):
        """Flushes the stderr message queue on a terminal"""
        for msg in sorted(queue.keys()):
            print(queue[msg][1], file=self._fp_err)

    def _flush_file(self):
        """Flush implementation for file logging (lazy)"""
        if not self._fp_std:
            self._fp_std = open(self._logfile, encoding=get_conf('DEFAULT_CHARSET'), mode='a+')
        padding = len("[{}] [     ]".format(datetime.now().strftime(get_conf('DEFAULT_LOG_TIMESTAMP')))) * " "
        queue = dict(**self._queue['err'])
        queue.update(self._queue['std'])
        for msg in sorted(queue.keys()):
            msg_lines = queue[msg][1].splitlines()
            print(
                "[{date}] [{level}] {message}".format(
                    date=datetime.now().strftime(get_conf('DEFAULT_LOG_TIMESTAMP')),
                    level=self._levels[queue[msg][0]][1],
                    message=msg_lines[0]
                ),
                file=self._fp_std
            )
            for msg_line in msg_lines[1:]:
                print("{padding} {message}".format(padding=padding, message=msg_line), file=self._fp_std)

    def _flush_syslog(self):
        """Flush implementation for syslog logging"""
        queue = dict(**self._queue['err'])
        queue.update(self._queue['std'])
        for msg in sorted(queue.keys()):
            syslog.syslog(getattr(syslog, self._levels[queue[msg][0]][2]), queue[msg][1])

    def log(self, level, message):
        """Register a log message within the logging queue"""
        # log usage messages only on a terminal
        if level == 'usage':
            if self._type == 'term':
                self._queue['err'][time.perf_counter()] = (level, message)
        # otherwise, log messages if their level is appropriate
        if level in self._levels and self._levels[self._level][0] >= self._levels[level][0]:
            if level == 'error':
                self._queue['err'][time.perf_counter()] = (level, message)
            else:
                self._queue['std'][time.perf_counter()] = (level, message)
        self._flush()

    def log_error(self, message):
        """Convenience shortcut for registering messages with log level `error`"""
        self.log('error', message)

    def log_warning(self, message):
        """Convenience shortcut for registering messages with log level `warning`"""
        self.log('warning', message)

    def log_notice(self, message):
        """Convenience shortcut for registering messages with log level `notice`"""
        self.log('notice', message)

    def log_info(self, message):
        """Convenience shortcut for registering messages with log level `info`"""
        self.log('info', message)

    def log_debug(self, message):
        """Convenience shortcut for registering messages with log level `debug`"""
        self.log('debug', message)

    def log_usage(self, message):
        """Convenience shortcut for registering messages with log level `usage`"""
        self.log('usage', message)

    @property
    def color(self):
        """
        Boolean switch indicating whether this logger allows colored output.
        """
        return self._color

    @color.setter
    def color(self, value):
        if termcolor.supports_color() and self._type == 'term' and type(value) == bool:
            self._color = value

    @property
    def facility(self):
        """
        The facility used for syslog.
        """
        return self._facility

    @facility.setter
    def facility(self, value):
        if hasattr(syslog, value):
            self._facility = value
            if self._type == 'syslog':
                self._close()
                self._open()

    @property
    def file(self):
        """
        The log file used when run as file logger.
        """
        return self._logfile

    @file.setter
    def file(self, value):
        self._logfile = value
        if self._type == 'file':
            self._close()
            self._open()

    @property
    def level(self):
        """
        The log level. Expected to be one of `mute`, `error`, `warning`, `info` or `debug`.
        """
        return self._level

    @level.setter
    def level(self, value):
        if value in self._levels:
            self._level = value

    @property
    def type(self):
        """
        The logger type. Expected to be one of `term`, `file` or `syslog`.
        """
        return self._type

    @type.setter
    def type(self, value):
        if value in ('file', 'term', 'syslog'):
            self._close()
            self._type = value
            self._open()
        if value in ('file', 'syslog'):
            self._color = False
