import logging
import os

class AppLogger(object):
    def __init__(self):
        """Do nothing, by default."""

    @staticmethod
    def log(msg):
        path = os.path.abspath('.')
        print  path
        m_logger = logging.getLogger('tshr_root')
        m_hdlr = logging.FileHandler(path+"\sina.log")
        m_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        m_hdlr.setFormatter(m_formatter)
        m_logger.addHandler(m_hdlr)
        m_logger.setLevel(logging.WARNING)
        m_logger.error(msg)
        m_hdlr.flush()
        m_logger.removeHandler(m_hdlr)
        m_hdlr.close()

if __name__ =="__main__":
    AppLogger.log("jinlong")
