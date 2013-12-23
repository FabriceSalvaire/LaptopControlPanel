####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import os

####################################################################################################

from .SysDevice import SysDevice

####################################################################################################

class PowerSources(dict):

    __sys_class_power_supply__ = '/sys/class/power_supply'

    ##############################################

    def __init__(self):

        super(PowerSources, self).__init__()

        for file_name in os.listdir(self.__sys_class_power_supply__):
            path = os.path.join(self.__sys_class_power_supply__, file_name)
            if file_name == 'AC':
                power_source = AcPower(path)
            else:
                power_source = Battery(path)
            self[power_source.name] = power_source

####################################################################################################

class PowerSource(SysDevice):

    ##############################################

    def __init__(self, path):

        super(PowerSource, self).__init__(path)

        self._type = self.read('type')

    ##############################################

    @property
    def type(self):
        return self._type

####################################################################################################

class AcPower(PowerSource):

    ##############################################

    @property
    def online(self):
        return self.read_bool('online')

####################################################################################################

class Battery(PowerSource):

    ##############################################

    @property
    def status(self):
        return self.read('status')

    ##############################################

    @property
    def present(self):
        return self.read_bool('present')

    ##############################################

    @property
    def technology(self):
        return self.read('technology')

    ##############################################

    @property
    def cycle_count(self):
        return self.read_int('cycle_count')

    ##############################################

    @property
    def voltage_min_design(self):
        return self.read_int('voltage_min_design')

    ##############################################

    @property
    def voltage_now(self):
        return self.read_int('voltage_now')

    ##############################################

    @property
    def power_now(self):
        return self.read_int('power_now')

    ##############################################

    @property
    def energy_full_design(self):
        return self.read_int('energy_full_design')

    ##############################################

    @property
    def energy_full(self):
        return self.read_int('energy_full')

    ##############################################

    @property
    def energy_now(self):
        return self.read_int('energy_now')

    ##############################################

    @property
    def capacity(self):
        return self.read_int('capacity')

    ##############################################

    @property
    def model_name(self):
        return self.read('model_name')

    ##############################################

    @property
    def manufacturer(self):
        return self.read('manufacturer')

    ##############################################

    @property
    def serial_number(self):
        return self.read('serial_number')

####################################################################################################
# 
# End
# 
####################################################################################################
