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

import numpy as np

####################################################################################################

from LaptopControlPanel.Tools.SleepThread import SleepThread

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class DataProvider(object):

    __name__ = None
    __dtype__ = None

    ##############################################

    def __str__(self):
        return self.__name__

    ##############################################

    @property
    def dtype(self):
        return self.__dtype__

    ##############################################

    def __call__(self):
        raise NotImplementedError

####################################################################################################

class RoundRobinMonitoring(SleepThread):

    _logger = _module_logger.getChild('RoundRobinMonitoring')

    ##############################################

    def __init__(self, time_resolution, time_period, data_providers):

        super(RoundRobinMonitoring, self).__init__(sleep_time=time_resolution)

        self.daemon = True
        
        self._time_period = time_period
        self._data_providers = [data_provider() for data_provider in data_providers]

        self._init_date_frame()
        self._previous_frame = False
        self._time_slot = 0

    ##############################################

    def _init_date_frame(self):

        dtype = [(str(data_provider), data_provider.dtype) for data_provider in self._data_providers]
        self._data_frame = np.zeros(self._time_period, dtype=dtype)

    ##############################################

    @property
    def time_resolution(self):
        return self.sleep_time

    ##############################################

    @property
    def period(self):
        return self._time_period

    ##############################################

    @property
    def time_slot(self):
        return self._time_slot

    ##############################################

    @property
    def last_time(self):

        if self._previous_frame:
            return self._time_period
        else:
            return self._time_slot

    ##############################################

    @property
    def times(self):

        return np.arange(self.last_time)

    ##############################################

    def field(self, name):

        time_slot = self._time_slot
        circular_buffer = self._data_frame[name]
        if self._previous_frame:
            time_slot_reciproqual = self._time_period - time_slot
            data = circular_buffer.copy()
            data[time_slot_reciproqual:] = circular_buffer[:time_slot]
            data[:time_slot_reciproqual] = circular_buffer[time_slot:]
            return data
        else:
            return circular_buffer[:time_slot]

    ##############################################

    def work(self):

        time_slot = self._time_slot
        self._logger.info("Time slot %u" % (time_slot))

        for data_provider in self._data_providers:
            self._data_frame[str(data_provider)][time_slot] = data_provider()

        # Circular buffer:
        # |0           -> | ts             | time period
        # | current frame | previous frame |

        # self._time_slot = (self._time_slot +1) % self._time_period
        time_slot += 1
        if time_slot == self._time_period:
            # start a new frame
            self._previous_frame = True
            self._time_slot = 0
        else:
            self._time_slot = time_slot

####################################################################################################
# 
# End
# 
####################################################################################################
