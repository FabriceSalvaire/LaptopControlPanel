####################################################################################################
# 
# LaptopControlPanel - @ProjectDescription@.
# Copyright (C) Fabrice Salvaire 2013 
# 
####################################################################################################

###################################################################################################

import logging

from PyQt4 import QtCore, QtGui

####################################################################################################

from .GuiApplicationBase import GuiApplicationBase
from LaptopControlPanel.Application.ApplicationBase import ApplicationBase

####################################################################################################

class Application(GuiApplicationBase, ApplicationBase):

    _logger = logging.getLogger(__name__)
    
    ###############################################
    
    def __init__(self, args):

        super(Application, self).__init__(args=args)
        self._logger.debug(str(args))
        
        from .MainWindow import MainWindow
        self._main_window = MainWindow()
        self._main_window.showMaximized()
        
        self.post_init()

    ##############################################

    def _init_actions(self):

        super(Application, self)._init_actions()

####################################################################################################
#
# End
#
####################################################################################################
