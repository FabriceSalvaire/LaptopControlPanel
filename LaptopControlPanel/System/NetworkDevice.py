####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import logging
import os
import subprocess

####################################################################################################

from .SysDevice import SysDevice

####################################################################################################

class NetworkDevices(dict):

    __sys_class_rfkill__ = '/sys/class/rfkill'

    ##############################################

    def __init__(self):

        super(NetworkDevices, self).__init__()

        for file_name in os.listdir(self.__sys_class_rfkill__):
            network_device = NetworkDevice(os.path.join(self.__sys_class_rfkill__, file_name))
            self[network_device.name] = network_device

####################################################################################################

class NetworkDevice(SysDevice):

    _logger = logging.getLogger(__name__)

    ##############################################

    def __init__(self, path):

        super(NetworkDevice, self).__init__(path)

        self._index = self._read_int('index')
        self._name = self._read('name')
        self._type = self._read('type')

    ##############################################

    @property
    def type(self):
        return self._type

    ##############################################

    @property
    def hard(self):
        return self._read_bool('hard')

    ##############################################

    @property
    def soft(self):
        return self._read_bool('soft')

    ##############################################

    @soft.setter
    def soft(self, status):

        if status:
            block_status = 'block'
        else:
            block_status = 'unblock'
        self._logger.info("Call rfkill %s %u for device %s" % (block_status, self._index, self.name))
        subprocess.check_call(['/sbin/rfkill', block_status, str(self._index)])

####################################################################################################
# 
# End
# 
####################################################################################################
