####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import logging
import threading
import time

####################################################################################################

from LaptopControlPanel.Kernel.Module import is_module_loaded, unload_module, load_module

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

        module = 'thinkpad-acpi'
        if is_module_loaded(module):
            unload_module(module)
        if not is_module_loaded(module):
            load_module(module, options=['fan_control=1'])

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

    ##############################################

    def calibrate(self):

        calibrate_thread = CalibrateThread(self)
        speeds = calibrate_thread.run()

        return speeds

####################################################################################################

class CalibrateThread(threading.Thread):

    _logger = _module_logger.getChild('CalibrateThread')

    ##############################################

    def __init__(self, fan_manager):

        super(CalibrateThread, self).__init__()
        self.daemon = True

        self._fan_manager = fan_manager

    ###############################################

    def run(self):

        sleep_time = 10 # s

        current_level = self._fan_manager.level
        speeds = []
        for level in list(range(8)) + ['full-speed']:
            self._fan_manager.level = level
            speed_t0 = self._fan_manager.speed
            while True:
                time.sleep(sleep_time)
                speed = self._fan_manager.speed
                self._logger.debug("Speed %u rpm" % (speed))
                if abs(speed_t0 - speed) < 1:
                    break
                else:
                    speed_t0 = speed
            self._logger.info("Level %s: %u rpm" % (str(level), speed))
            speeds.append(speed)
        self._fan_manager.level = current_level

        return speeds

####################################################################################################
# 
# End
# 
####################################################################################################
