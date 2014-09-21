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

####################################################################################################

class SysDevice(object):

    ##############################################

    def __init__(self, path):

        self._path = path
        self._name = os.path.basename(path)

    ##############################################

    @property
    def name(self):
        return self._name

    ##############################################

    def _join(self, file_name):

        return os.path.join(self._path, file_name)

    ##############################################

    def read(self, file_name):

        with open(self._join(file_name), 'r') as f:
            return f.read().strip()

    ##############################################

    def read_int(self, file_name):

        return int(self.read(file_name))

    ##############################################

    def read_bool(self, file_name):

        return bool(self.read_int(file_name))

####################################################################################################
# 
# End
# 
####################################################################################################
