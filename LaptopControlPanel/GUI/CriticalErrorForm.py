# -*- coding: utf-8 -*-

####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################
#
#                                              Audit
#
# - 25/05/2010 Fabrice
#   - exit button
#
####################################################################################################

####################################################################################################

import sys
import traceback

from PyQt4 import QtGui, QtCore

####################################################################################################

from LaptopControlPanel.Logging.ExceptionHook import format_exception
import LaptopControlPanel.Tools.BackTrace as BackTrace

####################################################################################################

from .ui.critical_error_form_ui import Ui_critical_error_form

####################################################################################################

class CriticalErrorForm(QtGui.QDialog, Ui_critical_error_form):

    ###############################################

    def __init__(self, exception_type, exception_value, exception_backtrace):

        QtGui.QDialog.__init__(self)

        self.setupUi(self)

        self._exception_type = exception_type
        self._exception_value = exception_value
        self._exception_backtrace = exception_backtrace
        self._backtrace = format_exception(self._exception_type,
                                           self._exception_value,
                                           self._exception_backtrace)
        
        # Fixme: call critical exit
        self.exit_button.clicked.connect(lambda : sys.exit(1))
        self.show_backtrace_button.clicked.connect(self.show_backtrace)

        title = str(exception_value)
        self.error_message_label.setText(title[:50])
        backtrace_text = ''.join(traceback.format_exception(exception_type,
                                                            exception_value,
                                                            exception_backtrace))

        self._trace_back_text_highlighted = BackTrace.html_highlight_backtrace(backtrace_text)

        self.back_trace_text_browser.clear()
        #!# self.back_trace_text_browser.hide()

    ###############################################

    def show_backtrace(self):

        # print trace_back_text_highlighted
        self.back_trace_text_browser.setHtml(self._trace_back_text_highlighted)

####################################################################################################
#
# End
#
####################################################################################################
