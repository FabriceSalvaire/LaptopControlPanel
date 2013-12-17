####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import logging

from PyQt4 import QtCore, QtGui

####################################################################################################

from .GuiApplicationBase import GuiApplicationBase
from .Widgets.IconLoader import IconLoader
from LaptopControlPanel.Application.ApplicationBase import ApplicationBase
from LaptopControlPanel.Tools.Units import minute

####################################################################################################

class Application(GuiApplicationBase, ApplicationBase):

    _logger = logging.getLogger(__name__)
    
    ###############################################
    
    def __init__(self, args):

        super(Application, self).__init__(args=args)
        self._logger.debug(str(args))

        self.timer = QtCore.QTimer()
        self.timer.start(minute(1))
        self.timer.timeout.connect(self._refresh)

        self._icon_loader = IconLoader()
        
        from .MainWindow import MainWindow
        self._main_window = MainWindow()
        self._main_window.showMaximized()

        self._post_init_actions()
        self._init_tray_icon()
       
        self.post_init()

    ##############################################

    def _init_actions(self):

        super(Application, self)._init_actions()

    ##############################################

    def _post_init_actions(self):

        self._restore_action = QtGui.QAction("&Restore",
                                             self._main_window,
                                             triggered=self._main_window.show,
                                             )

    ##############################################

    def _init_tray_icon(self):

        if QtGui.QSystemTrayIcon.isSystemTrayAvailable():
            menu = QtGui.QMenu(self._main_window)
            # menu.addAction(self.minimize_action)
            # menu.addAction(self.maximize_action)
            menu.addAction(self._restore_action)
            menu.addSeparator()
            menu.addAction(self.quit_action)
            
            icon = self._icon_loader.get_icon('tools', icon_size=64)
            
            self._tray_icon = QtGui.QSystemTrayIcon(icon, self._main_window)
            self._tray_icon.setContextMenu(menu)
            self._tray_icon.show()
        else:
            self._logger.info("System tray is not available")
            self._tray_icon = None

    ##############################################

    @property
    def tray_icon(self):
        return self._tray_icon

    ##############################################

    @property
    def icon_loader(self):
        return self._icon_loader
     
    ##############################################

    def _refresh(self):

        self._logger.info('Refresh State')

####################################################################################################
#
# End
#
####################################################################################################
