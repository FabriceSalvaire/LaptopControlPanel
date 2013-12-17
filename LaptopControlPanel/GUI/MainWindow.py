# -*- coding: utf-8 -*-

####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

from PyQt4 import QtCore, QtGui

####################################################################################################

from .MainWindowBase import MainWindowBase
# from .Pages.Page import PageMetaClass

####################################################################################################

class MainWindow(MainWindowBase):

    ##############################################

    def __init__(self):

        super(MainWindow, self).__init__(title='LaptopControlPanel')

        self._init_ui()

    ##############################################

    def init_menu(self):

        super(MainWindow, self).init_menu()

    ##############################################

    def _init_ui(self):

        self.statusBar()

        central_widget = QtGui.QWidget(self)
        self.setCentralWidget(central_widget)
        horizontal_Layout = QtGui.QHBoxLayout(central_widget)

        self._list_widget = QtGui.QListWidget(central_widget)
        self._list_widget.setMaximumSize(QtCore.QSize(200, 16777215))

        self._stacked_widget = QtGui.QStackedWidget(central_widget)

        self._list_widget.currentRowChanged.connect(self._stacked_widget.setCurrentIndex)

        from .Pages.NetworkDevicePage import NetworkDevicePage
        from .Pages.PowerSourcePage import PowerSourcePage
        # for page_class in PageMetaClass.pages.itervalues():
        for page_class in (NetworkDevicePage,
                           PowerSourcePage,
                           ):
            item = QtGui.QListWidgetItem(page_class.__page_title__)
            self._list_widget.addItem(item)
            page = page_class(central_widget)
            self._stacked_widget.addWidget(page)
            
        for widget in self._list_widget, self._stacked_widget:
            horizontal_Layout.addWidget(widget)

        self._application.timer.timeout.connect(self._refresh)

        self._translate_ui()

    ##############################################

    def _translate_ui(self):

        pass
        # self.foo.setText(self.translate("..."))

    ##############################################

    def closeEvent(self, event=None):

        tray_icon = self._application.tray_icon
        if tray_icon is not None and tray_icon.isVisible():
            # Fixme: Config.Title
            # QtGui.QMessageBox.information(self, "Laptop Control Panel",
            #                               "The program will keep running in the system tray. To "
            #                               "terminate the program, choose <b>Quit</b> in the "
            #                               "context menu of the system tray entry.")
            self.hide()
            event.ignore()
        else:
            self._application.exit()

    ##############################################

    def _refresh(self):

        self._stacked_widget.currentWidget().refresh()

####################################################################################################
#
# End
#
####################################################################################################
