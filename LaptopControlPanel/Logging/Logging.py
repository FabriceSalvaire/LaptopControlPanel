####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import yaml
import logging
import logging.config

####################################################################################################

from .ExceptionHook import DispatcherExceptionHook, StderrExceptionHook
from LaptopControlPanel.Tools.Singleton import singleton
import LaptopControlPanel.Config.ConfigInstall as ConfigInstall

####################################################################################################

@singleton
class ExceptionHookInitialiser(object):

    ##############################################

    def __init__(self, context, stderr=True):

        self._context = context
        self._dispatcher_exception_hook = DispatcherExceptionHook()

        if stderr:
            stderr_exception_hook = StderrExceptionHook()
            self._dispatcher_exception_hook.register_observer(stderr_exception_hook)

####################################################################################################

def setup_logging(application_name, config_file=ConfigInstall.Logging.default_config_file):

    logging_config_file_name = ConfigInstall.Logging.find(config_file)
    logging_config = yaml.load(open(logging_config_file_name, 'r'))

    # Fixme: \033 is not interpreted in YAML
    formatter_config = logging_config['formatters']['ansi']['format']
    logging_config['formatters']['ansi']['format'] = formatter_config.replace('<ESC>', '\033')
    logging.config.dictConfig(logging_config)

    logger = logging.getLogger(application_name)
    logger.info('Start %s' % (application_name))

    return logger

####################################################################################################
#
# End
#
####################################################################################################
