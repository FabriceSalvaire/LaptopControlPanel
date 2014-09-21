# -*- coding: utf-8 -*-

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
