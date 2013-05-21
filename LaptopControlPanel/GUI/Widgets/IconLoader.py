####################################################################################################
# 
# LaptopControlPanel - @ProjectDescription@.
# Copyright (C) Fabrice Salvaire 2013 
# 
####################################################################################################

""" Inspired from KIcon.
"""

####################################################################################################

from PyQt4 import QtGui

####################################################################################################

from LaptopControlPanel.Tools.Singleton import SingletonMetaClass
import LaptopControlPanel.Config.ConfigInstall as ConfigInstall

####################################################################################################

class IconLoader(object):

    __metaclass__ = SingletonMetaClass

    icon_size = 22

    ##############################################

    def __init__(self):

        self._cache = {}

    ##############################################

    def _mangle_icon_name(self, icon_name, icon_size):

        return icon_name + '@%u' % icon_size

    ##############################################

    def _demangle_icon_name(self, icon_name):

        if '@' in icon_name:
            icon_name, icon_size = icon_name.split('@')
            icon_size = int(icon_size)
        else:
            icon_size = self.icon_size

        return icon_name, icon_size

    ##############################################

    def __getitem__(self, icon_name):

        icon_name, icon_size = self._demangle_icon_name(icon_name)
        return self.get_icon(icon_name, icon_size)

    ##############################################

    def get_icon(self, icon_name, icon_size=icon_size):

        mangled_icon_name = self._mangle_icon_name(icon_name, icon_size)
        if mangled_icon_name not in self._cache:
            icon_path = self._find(icon_name, icon_size)
            self._cache[mangled_icon_name] = QtGui.QIcon(icon_path)

        return self._cache[mangled_icon_name]

    ##############################################

    def _find(self, file_name, icon_size, extension='.png'):

        return ConfigInstall.Icon.find(file_name + extension, icon_size)

####################################################################################################
# 
# End
# 
####################################################################################################
