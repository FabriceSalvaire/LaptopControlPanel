####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
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
