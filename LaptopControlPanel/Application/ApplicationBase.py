# -*- coding: utf-8 -*-

####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
