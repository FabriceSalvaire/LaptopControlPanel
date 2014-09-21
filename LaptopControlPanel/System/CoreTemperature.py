# -*- coding: utf-8 -*-

####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
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
