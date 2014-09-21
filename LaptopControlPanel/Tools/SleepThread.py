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

import threading
import time

####################################################################################################

class SleepThread(threading.Thread):

    """A SleepThread run an infinite loop which sleep during some time and call the
    abstract method :meth:`work`.
    """

    ###############################################

    def __init__(self, sleep_time=60):

        super(SleepThread, self).__init__()

        self.sleep_time = sleep_time

        self._stop = threading.Event()

    ##############################################

    def stop(self):
        self._stop.set()
        
    ###############################################

    def run(self):

        while not self._stop.is_set():
            self.work()
            time.sleep(self.sleep_time)

    ###############################################

    def work(self):

        raise NotImplementedError
        
####################################################################################################
#
# End
#
####################################################################################################
