####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
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
