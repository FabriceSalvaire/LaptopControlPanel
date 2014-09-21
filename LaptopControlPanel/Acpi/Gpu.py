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
import os

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class GpuManager(object):

    _logger = _module_logger.getChild('GpuManager')

    __bbswitch_file__ = '/proc/acpi/bbswitch'

    ##############################################

    @staticmethod
    def has_bbswitch():
        return os.path.exists(GpuManager.__bbswitch_file__)

    ##############################################

    @staticmethod
    def state():
        
        with open(GpuManager.__bbswitch_file__, 'r') as f:
            line = f.readline()
            if 'ON' in line:
                return True
            elif 'OFF' in line:
                return False
            else:
                raise NameError('Unknown bbswitch state')

    ##############################################

    @staticmethod
    def set_state(state):

        action = 'ON 'if state else 'OFF'
        with open(GpuManager.__bbswitch_file__, 'w') as f:
            GpuManager._logger.info('Set GPU %s' % (action))
            f.write(action)

####################################################################################################
# 
# End
# 
####################################################################################################
