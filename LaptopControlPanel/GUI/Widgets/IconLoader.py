####################################################################################################
# 
# LaptopControlPanel - @ProjectDescription@.
# Copyright (C) Fabrice Salvaire 2013 
# 
####################################################################################################

""" Inspired from KIcon.
"""

####################################################################################################

from PyQt4 import QtCore, QtGui

####################################################################################################

from LaptopControlPanel.Tools.Singleton import singleton
import LaptopControlPanel.Config.ConfigInstall as ConfigInstall

####################################################################################################

@singleton
class IconLoader(object):

    ##############################################

    def __init__(self):

        self._cache = {}

    ##############################################

    def __getitem__(self, file_name):

        if file_name not in self._cache:
            absolut_file_name = self._find(file_name)
            self._cache[file_name] = QtGui.QIcon(absolut_file_name)
        return self._cache[file_name]

    ##############################################

    def _find(self, file_name, extension='.png'):

        return ConfigInstall.Icon.find(file_name + extension)

####################################################################################################
# 
# End
# 
####################################################################################################
