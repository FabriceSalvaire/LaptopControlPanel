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

####################################################################################################

from .BatteryStatusDataBase import BatteryStatusDataBase
from LaptopControlPanel.System.PowerSource import PowerSources
from LaptopControlPanel.System.Proc import LoadAverage
from LaptopControlPanel.Tools.SleepThread import SleepThread

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class BatteryMonitor(SleepThread):

    _logger = _module_logger.getChild('BatteryMonitor')

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
