####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import logging
import time

import numpy as np
import pandas as pd

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

        self._data_frame = None
        self._start_time = None
        self._time_slot = 0

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
    def data_frame(self):
        return self._data_frame

    ##############################################

    @property
    def time_slot(self):
        return self._time_slot

    ##############################################

    def _init_date_frame(self):

        self._start_time = time.time()
        # current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # index = pd.date_range(current_time, periods=self._time_period, freq='%us' % self.time_resolution)
        self._data_frame = pd.DataFrame({str(data_provider): np.zeros(self._time_period, dtype=data_provider.dtype)
                                         for data_provider in self._data_providers},
                                        # index=index, # then indexing must be timestamp
                                        )

    ##############################################

    def work(self):

        if self._start_time is None:
            self._init_date_frame()
        # current_time = time.time()
        # time_slot = int((current_time - self._start_time) / self.time_resolution) % self._time_period
        time_slot = self._time_slot

        self._logger.info("Time slot %u" % (time_slot))

        for data_provider in self._data_providers:
            self._data_frame[str(data_provider)][time_slot] = data_provider()

        self._time_slot = (self._time_slot +1) % self._time_period

####################################################################################################
# 
# End
# 
####################################################################################################
