# -*- coding: utf-8 -*-

####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import os
import re
import subprocess

####################################################################################################

class HddManager(object):

    ##############################################

    def __init__(self, device_name='sda'):

        self._device_name = device_name

    ##############################################

    @property
    def device_path(self):
        return os.path.join('/dev', self._device_name)
    
    ##############################################

    def temperature(self):

        process = subprocess.Popen(('hddtemp', self.device_path),
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        stdout, stderr = process.communicate()
        # '/dev/sda: HGST HTS725050A7E630: 36°C'
        match = re.match('.*: (\d+).+C$', stdout.strip())
        if match is not None:
            return int(match.groups()[0])
        else:
            NameError("Cannot decode hddtemp output")

####################################################################################################
# 
# End
# 
####################################################################################################
