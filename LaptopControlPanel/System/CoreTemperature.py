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

from .SysDevice import SysDevice
from LaptopControlPanel.Kernel.Module import is_module_loaded, load_module

####################################################################################################

class CoreTemperature(SysDevice):

    __path__ = '/sys/devices/platform/coretemp.0/hwmon/hwmon2'

    ##############################################

    def __init__(self):

        super(CoreTemperature, self).__init__(self.__path__)
        self._load_coretemp_module()

    ##############################################

    def _load_coretemp_module(self):

        module = 'coretemp'
        if not is_module_loaded(module):
            load_module(module)

    ##############################################

    @property
    def temperature(self):
        return self.read_int('temp1_input') / 1000

####################################################################################################
# 
# End
# 
####################################################################################################
