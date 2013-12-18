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

class FanManager(object):

    _logger = _module_logger.getChild('FanManager')

    __fan_file__ = '/proc/acpi/ibm/fan'

    ##############################################

    def __init__(self):

        #!# self._load_thinkpad_acpi_module()
        self._get_state()

    ##############################################

    @property
    def speed(self):
        self._get_state()
        return self._speed

    ##############################################

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._set_level(level)

    ##############################################

    def _load_thinkpad_acpi_module(self):

        # /!\ This code has side-effect on keyboard (AltGr)

        self._logger.debug("Load module thinkpad-acpi")
        rc = subprocess.check_call(['/sbin/rmmod', 'thinkpad-acpi'])
        # if rc:
        #     raise NameError("Cannot unload thinkpad-acpi")
        rc = subprocess.check_call(['/sbin/modprobe', 'thinkpad-acpi', 'fan_control=1'])
        if rc:
            raise NameError("Cannot load module thinkpad-acpi")

    ##############################################

    def _get_value(self, line):

        return line.split(':')[-1].strip()

    ##############################################

    def _get_state(self):

        with open(self.__fan_file__, 'r') as f:
            for line in f:
                if line.startswith('status:'):
                    self._status = self._get_value(line)
                if line.startswith('speed:'):
                    self._speed = int(self._get_value(line))
                if line.startswith('level:'):
                    # level is 0-7, auto, disengaged, full-speed
                    self._level = self._get_value(line)

    ##############################################

    def _set_level(self, level):

        level = str(level)
        self._logger.info("Set level %s" % (level))
        values = [str(x) for x in range(8)] + ['auto', 'disengaged', 'full-speed']
        if level not in values:
            raise ValueError()

        with open(self.__fan_file__, 'w') as f:
            f.write('level ' + level)
        self._get_state()

####################################################################################################
# 
# End
# 
####################################################################################################
