####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
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
            time.sleep(self.sleep_time)
            self.work()

    ###############################################

    def work(self):

        raise NotImplementedError
        
####################################################################################################
#
# End
#
####################################################################################################
