# -*- coding: utf-8 -*-

####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import logging
import sys
import traceback

####################################################################################################

class ApplicationBase(object):

    _logger = logging.getLogger(__name__)

    has_gui = False
    
    ##############################################
    
    def __init__(self, args, **kwargs):

        self._logger.debug(str(args) + ' ' + str(kwargs))

        sys.excepthook = self._exception_hook

        self._args = args

    ##############################################

    @property
    def args(self):
        return self._args

    ##############################################

    def _exception_hook(self, exception_type, exception_value, exception_traceback):

        traceback.print_exception(exception_type, exception_value, exception_traceback)

    ##############################################
    
    def exit(self):

        sys.exit(0)

    ##############################################

    def show_message(self, message=None, **kwargs):

        self._logger.info(message)
        
####################################################################################################
#
# End
#
####################################################################################################
