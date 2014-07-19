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
import datetime
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
        if termcolor.supports_color() and self._type == 'term':
            self._color = True
        else:
            self._color = False
        self._open()

    def _open(self):
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
        if self._type == 'term':
            self._fp_std = None
            self._fp_err = None
        elif self._type == 'file':
            self._fp_std.close()
            self._fp_err = None
        elif self._type == 'syslog':
            syslog.closelog()

    def _flush(self):
        if self._type == 'term':
            self._flush_term()
        elif self._type == 'file':
            self._flush_file()

    def _flush_term(self):
        self._flush_term_err(self._queue['err'])
        self._flush_term_std(self._queue['std'])

    def _flush_term_std(self, queue):
        for msg in sorted(queue.keys()):
            print(queue[msg][1], file=self._fp_std)

    def _flush_term_err(self, queue):
        for msg in sorted(queue.keys()):
            print(queue[msg][1], file=self._fp_err)

    def _flush_file(self):
        if not self._fp_std:
            self._fp_std = open(self._logfile, encoding=get_conf('DEFAULT_CHARSET'), mode='a+')
        padding = len("[{}] [     ]".format(
            datetime.datetime.strftime(datetime.datetime.now(), get_conf('DEFAULT_LOG_TIMESTAMP'))
        )) * " "
        queue = dict(**self._queue['err'])
        queue.update(self._queue['std'])
        for msg in sorted(queue.keys()):
            msg_lines = queue[msg][1].splitlines()
            print(
                "[{date}] [{level}] {message}".format(
                    date=datetime.datetime.strftime(datetime.datetime.now(), get_conf('DEFAULT_LOG_TIMESTAMP')),
                    level=self._levels[queue[msg][0]][1],
                    message=msg_lines[0]
                ),
                file=self._fp_std
            )
            for msg_line in msg_lines[1:]:
                print("{padding} {message}".format(padding=padding, message=msg_line), file=self._fp_std)

    def _flush_syslog(self):
        queue = dict(**self._queue['err'])
        queue.update(self._queue['std'])
        for msg in sorted(queue.keys()):
            syslog.syslog(getattr(syslog, self._levels[queue[msg][0]][2]), queue[msg][1])

    def log(self, level, message):
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
        self.log('error', message)

    def log_warning(self, message):
        self.log('warning', message)

    def log_notice(self, message):
        self.log('notice', message)

    def log_info(self, message):
        self.log('info', message)

    def log_debug(self, message):
        self.log('debug', message)

    def log_usage(self, message):
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
