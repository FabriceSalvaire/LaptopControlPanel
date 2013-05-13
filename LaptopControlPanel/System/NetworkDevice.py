####################################################################################################
# 
# @Project@ - @ProjectDescription@.
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

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

    ##############################################

    def __init__(self, path):

        super(NetworkDevice, self).__init__(path)

        self._index = self._read('index')
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
            block_status = 'unblock'
        else:
            block_status = 'block'
        subprocess.check_call(['/sbin/rfkill', block_status, self._index])

####################################################################################################
# 
# End
# 
####################################################################################################
