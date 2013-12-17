####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import logging

####################################################################################################

from .BatteryStatusDataBase import BatteryStatusDataBase
from LaptopControlPanel.System.PowerSource import PowerSources
from LaptopControlPanel.System.Proc import LoadAverage
from LaptopControlPanel.Tools.SleepThread import SleepThread

####################################################################################################

class BatteryMonitor(SleepThread):

    _logger = logging.getLogger(__name__ + '.BatteryMonitor')

    ##############################################

    def __init__(self, database_path, time_resolution):

        super(BatteryMonitor, self).__init__(sleep_time=time_resolution)

        self.daemon = True

        self._battery_database = BatteryStatusDataBase(database_path)
        self._battery_status_table = self._battery_database.battery_status_table

        self._power_sources = PowerSources()
        self._battery = self._power_sources['BAT0']

        self._load_average = LoadAverage()

    ##############################################

    @property
    def time_resolution(self):
        return self.sleep_time

    ##############################################

    def work(self):

        self._load_average.update()

        d = dict(battery_capacity=self._battery.capacity,
                 time_resolution=self.time_resolution,
                 load_average_1_min=self._load_average.number_of_job_1_min,
                 load_average_5_min=self._load_average.number_of_job_5_min,
                 load_average_15_min=self._load_average.number_of_job_15_min,
                 )
        self._logger.info(str(d))
        self._battery_status_table.add_new_row(**d)

####################################################################################################
# 
# End
# 
####################################################################################################
