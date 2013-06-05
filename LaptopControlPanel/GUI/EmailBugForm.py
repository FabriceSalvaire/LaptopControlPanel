# -*- coding: utf-8 -*-

####################################################################################################
# 
# LaptopControlPanel - @ProjectDescription@.
# Copyright (C) Fabrice Salvaire 2013 
# 
####################################################################################################

####################################################################################################

from PyQt4 import QtGui

####################################################################################################

from LaptopControlPanel.Logging.Email import Email
from LaptopControlPanel.Tools.Platform import Platform
import LaptopControlPanel.Config.Config as Config
import LaptopControlPanel.Version as Version

####################################################################################################

from .ui.email_bug_form_ui import Ui_email_bug_form

####################################################################################################

class EmailBugForm(QtGui.QDialog):

    ###############################################

    def __init__(self, traceback=''):

        super(EmailBugForm, self).__init__()

        self._traceback = traceback

        form = self._form = Ui_email_bug_form()
        form.setupUi(self)

        form.send_email_button.clicked.connect(self.send_email)

    ##############################################

    def send_email(self):

        form = self._form

        from_address = str(form.from_line_edit.text())
        if not from_address:
            from_address = Config.Email.from_address
        
        # Fixme: test field ?
        # QtGui.QMessageBox.critical(None, title, message)

        template_message = """
Bug description:
%(description)s

---------------------------------------------------------------------------------
LaptopControlPanel Version:
  %(software_version)s

---------------------------------------------------------------------------------
%(traceback)s

---------------------------------------------------------------------------------
%(platform)s

---------------------------------------------------------------------------------
"""

        application = QtGui.QApplication.instance()

        # Fixme: singleton ?
        platform = Platform(application)
        platform.query_opengl()
       
        message = template_message % {'description': str(form.description_plain_text_edit.toPlainText()),
                                      'software_version': str(Version.software_version),
                                      'platform': str(platform),
                                      'traceback': self._traceback,
                                      }

        email = Email(from_address=from_address,
                      subject='LaptopControlPanel Bug: ' + str(form.subject_line_edit.text()),
                      recipients=Config.Email.to_address,
                      message=message,
                      )
        recipients = str(form.recipients_line_edit.text())
        if recipients:
            email.add_recipients_from_string(recipients)
        email.send()

        self.accept()

####################################################################################################
#
# End
#
####################################################################################################
