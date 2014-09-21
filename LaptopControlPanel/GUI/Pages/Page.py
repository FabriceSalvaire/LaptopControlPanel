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

from PyQt4 import QtGui

####################################################################################################

class PageMetaClass(type):

    pages = {}

    ##############################################

    def __init__(cls, class_name, super_classes, class_attribute_dict):

        type.__init__(cls, class_name, super_classes, class_attribute_dict)
        PageMetaClass.pages[cls.__page_name__] = cls

####################################################################################################

class PageBase(QtGui.QWidget):

    # __metaclass__ = PageMetaClass

    __page_name__ = None
    __page_title__ = None

    ##############################################

    def __init__(self, parent=None):

       super(PageBase, self).__init__(parent)

       # Fixme: use _

       self._application = QtGui.QApplication.instance()
       self._main_window = self._application.main_window

####################################################################################################
# 
# End
# 
####################################################################################################
