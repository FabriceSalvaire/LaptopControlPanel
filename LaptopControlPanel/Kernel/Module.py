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
import os
import subprocess

####################################################################################################

__all__ = ['is_module_loaded', 'unload_module', 'load_module']

####################################################################################################

__rmmod__ = '/sbin/rmmod'
__modprobe__ = '/sbin/modprobe'

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

def is_module_loaded(module):

    return os.path.exists(os.path.join('/sys/module', module))

####################################################################################################

def unload_module(module):

    _module_logger.debug('Unload module %s' % (module))
    command = [__rmmod__, module]
    rc = subprocess.check_call(command)
    if rc:
        raise NameError("Cannot unload %s" % (module))

####################################################################################################

def load_module(module, options=None):

    _module_logger.debug('Load module %s' % (module))
    command = [__modprobe__, module]
    if options is not None:
        command += options
    rc = subprocess.check_call(command)
    if rc:
        raise NameError("Cannot load module %s" % (module))

####################################################################################################
# 
# End
# 
####################################################################################################
