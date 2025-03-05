import logging
import logging.handlers
from pythonjsonlogger import jsonlogger
import sys
import socket
from syslog import LOG_USER
from pathlib import Path


class VulnLogger:
    Path("log").mkdir(parents=True, exist_ok=True)
    __system_logger = logging.getLogger("VulnScanner-Logger")
    __system_logger.setLevel(logging.INFO)
    __system_logger_formatter = logging.Formatter('%(asctime)s %(message)s')
    #__system_logger_formatter = jsonlogger.JsonFormatter()
    __system_logger_handler = logging.handlers.RotatingFileHandler(filename="log/vscan-controller.log",
                                                                   maxBytes=256000000, backupCount=7)
    __system_logger_handler.setFormatter(__system_logger_formatter)
    __system_logger.addHandler(__system_logger_handler)

    def __init__(self, name: str, log_host, log_port, ident):
        log_host = log_host
        csoc_logger = logging.getLogger(name)
        csoc_logger.setLevel(logging.INFO)
        # csoc_handler = SysLogHandler(address=(log_host, int(log_port)), facility=LOG_USER, socktype=socket.SOCK_STREAM)
        csoc_handler = ReconnectingSysLogHandler(address=(log_host, int(log_port)), facility=LOG_USER,
                                                 socktype=socket.SOCK_STREAM)
        csoc_handler.ident = ident + ":"
        csoc_logger.addHandler(csoc_handler)
        self.csoc_logger = csoc_logger

    def csocLog(self, priority: int, message: str):
        try:
            if priority == 0:
                self.csoc_logger.critical(message)
            elif priority == 1:
                self.csoc_logger.error(message)
            elif priority == 2:
                self.csoc_logger.warning(message)
            elif priority == 3:
                self.csoc_logger.info(message)
            else:
                self.csoc_logger.debug(message)
            return True
        except Exception as e:
            return False

    def sysLog(self, message: str):
        self.__system_logger.info(message)


class ReconnectingSysLogHandler(logging.handlers.SysLogHandler):
    """Syslog handler that reconnects if the socket closes

    If we're writing to syslog with TCP and syslog restarts, the old TCP socket
    will no longer be writeable and we'll get a socket.error of type 32.  When
    than happens, use the default error handling, but also try to reconnect to
    the same host/port used before.  Also make 1 attempt to re-send the
    message.
    """

    def __init__(self, *args, **kwargs):
        super(ReconnectingSysLogHandler, self).__init__(*args, **kwargs)
        self._is_retry = False

    def _reconnect(self):
        # print("reconnecting to log server")
        """Make a new socket that is the same as the old one"""
        # close the existing socket before getting a new one to the same host/port
        if self.socket:
            self.socket.close()

        # cut/pasted from logging.handlers.SysLogHandler
        if self.unixsocket:
            self._connect_unixsocket(self.address)
        else:
            self.socket = socket.socket(socket.AF_INET, self.socktype)
            if self.socktype == socket.SOCK_STREAM:
                # print("SOCK ADDRESS", self.address)
                self.socket.connect(self.address)

    def handleError(self, record):
        # use the default error handling (writes an error message to stderr)
        super(ReconnectingSysLogHandler, self).handleError(record)

        # If we get an error within a retry, just return.  We don't want an
        # infinite, recursive loop telling us something is broken.
        # This leaves the socket broken.
        if self._is_retry:
            # print("LOG RECORD IN RETRY:", record)
            return

        # Set the retry flag and begin deciding if this is a closed socket, and
        # trying to reconnect.
        self._is_retry = True
        try:
            __, exception, __ = sys.exc_info()
            # If the error is a broken pipe exception (32), get a new socket.
            if isinstance(exception, socket.error) and exception.errno == 32:
                try:
                    self._reconnect()
                except:
                    # If reconnecting fails, give up.
                    # print("LOG RETRY FAILED:", record)
                    raise
                else:
                    # Make an effort to rescue the recod.
                    # print("LOG EMIT!")
                    self.emit(record)
        finally:
            self._is_retry = False
