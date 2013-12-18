####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import logging
import subprocess

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class GpuManager(object):

    _logger = _module_logger.getChild('GpuManager')

    __bbswitch_file__ = '/proc/acpi/bbswitch'

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
