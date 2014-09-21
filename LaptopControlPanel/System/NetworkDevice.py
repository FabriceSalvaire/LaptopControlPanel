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

        self._index = self.read_int('index')
        self._name = self.read('name')
        self._type = self.read('type')

    ##############################################

    @property
    def type(self):
        return self._type

    ##############################################

    @property
    def hard(self):
        return self.read_bool('hard')

    ##############################################

    @property
    def soft(self):
        return self.read_bool('soft')

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
