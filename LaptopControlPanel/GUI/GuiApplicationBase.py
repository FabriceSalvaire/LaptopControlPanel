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

###################################################################################################
#
# If an exception is raise before application.exec then application exit.
#
####################################################################################################

####################################################################################################

import logging
import sys
import traceback

from PyQt4 import QtGui, QtCore

####################################################################################################

from .CriticalErrorForm import CriticalErrorForm
from LaptopControlPanel.Application.ApplicationBase import ApplicationBase
import LaptopControlPanel.Config.Config as Config
import LaptopControlPanel.Config.Messages as Messages
import LaptopControlPanel.Version as Version

# Load RC
#import .ui.project_rc

####################################################################################################

class GuiApplicationBase(ApplicationBase, QtGui.QApplication):

    _logger = logging.getLogger(__name__)

    has_gui = True
    
    ##############################################
    
    def __init__(self, args, **kwargs):

        super(GuiApplicationBase, self).__init__(args=args, **kwargs)
        # Fixme: Why ?
        self._logger.debug("QtGui.QApplication " + str(sys.argv))
        QtGui.QApplication.__init__(self, sys.argv)
        self._logger.debug('GuiApplicationBase ' + str(args) + ' ' + str(kwargs))

        self._display_splash_screen()

        self._main_window = None
        self._init_actions()

    ##############################################

    @property
    def main_window(self):
        return self._main_window

    ##############################################

    def _exception_hook(self, exception_type, exception_value, exception_traceback):

        traceback.print_exception(exception_type, exception_value, exception_traceback)
        dialog = CriticalErrorForm(exception_type, exception_value, exception_traceback)
        dialog.exec_()

        # return sys.__excepthook__(exception_type, exception_value, exception_traceback)

    ##############################################

    def _display_splash_screen(self):

        pixmap = QtGui.QPixmap(':/splash screen/images/splash_screen.png')
        self._splash = QtGui.QSplashScreen(pixmap)
        self._splash.show()
        self._splash.showMessage('<h2>LaptopControlPanel %(version)s</h2>' % {'version':str(Version.software_version)})
        self.processEvents()

    ##############################################

    def _init_actions(self):

        self.quit_action = \
            QtGui.QAction('&Quit',
                          self,
                          # triggered=QtGui.qApp.quit,
                          triggered=self.exit)

        self.about_action = \
            QtGui.QAction('About',
                          self,
                          triggered=self.about)

        self.help_action = \
            QtGui.QAction('Help',
                          self,
                          triggered=self.open_help)

    ##############################################
    
    def post_init(self):
         
        self._splash.finish(self._main_window)
        self.processEvents()
        del self._splash

        self.show_message('Welcome to LaptopControlPanel')

        # return to main and then enter to event loop
        
    ##############################################

    def show_message(self, message=None, echo=False, timeout=0):

        if self._main_window is not None:
            self._main_window.show_message(message, echo, timeout)

    ##############################################
    
    # Fixme: CriticalErrorForm vs critical_error

    def critical_error(self, title='LaptopControlPanel Critical Error', message=''):
        
        QtGui.QMessageBox.critical(None, title, message)
        
        # Fixme: qt close?
        sys.exit(1)

    ##############################################

    def open_help(self):

        url = QtCore.QUrl()
        url.setScheme(Config.Help.url_scheme)
        url.setHost(Config.Help.host)
        url.setPath(Config.Help.url_path_pattern) # % str(Version.software_version))
        #!# QtGui.QDesktopServices.openUrl(url)

    ##############################################

    def about(self):

        message = Messages.about % {'version':str(Version.software_version)}
        QtGui.QMessageBox.about(self.main_window, 'About LaptopControlPanel', message)

####################################################################################################
#
# End
#
####################################################################################################
