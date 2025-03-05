import logging
import logging.handlers
import sys
from logging.handlers import SysLogHandler
import socket
from syslog import LOG_USER
from pathlib import Path


class VulnSysLogger:
    Path("log").mkdir(parents=True, exist_ok=True)
    __system_logger = logging.getLogger("VulnScanner-SysLogger")
    __system_logger.setLevel(logging.INFO)
    __system_logger_formatter = logging.Formatter('%(asctime)s %(message)s')
    __system_logger_handler = logging.handlers.RotatingFileHandler(filename="log/vscan-controller.log",
                                                                   maxBytes=256000000, backupCount=7)
    __system_logger_handler.setFormatter(__system_logger_formatter)
    __system_logger.addHandler(__system_logger_handler)

    def __init__(self, name: str, ident):
        csoc_logger = logging.getLogger(name)
        csoc_logger.setLevel(logging.INFO)
        # csoc_handler = SysLogHandler(address=(log_host, int(log_port)), facility=LOG_USER, socktype=socket.SOCK_STREAM)
        csoc_handler = logging.handlers.RotatingFileHandler(filename="/var/log/csoc-vscan/csoc-vscan.json", maxBytes=1024000000, backupCount=2)
        #csoc_handler = ReconnectingSysLogHandler(address=(log_host, int(log_port)), facility=LOG_USER,
        #                                         socktype=socket.SOCK_STREAM)
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