####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import re
import smtplib

from email.mime.text import MIMEText

####################################################################################################

class Email(object):

    ##############################################

    def __init__(self,
                 from_address='',
                 subject='',
                 recipients=[],
                 message='',
                 ):

        self.check_email_is_valid(from_address)

        self._from_address = from_address
        self._subject = subject
        self.message = message

        self._recipients = []
        self.add_recipients(recipients)

    ##############################################

    def check_email_is_valid(self, email):

        return re.match('^[\w\.\-]+@[\w\.\-]+$', email) is not None

    ##############################################

    def add_recipients(self, recipients):

        for email in recipients:
            if not self.check_email_is_valid(email):
                raise ValueError("Email '%s' is not valid" % (email))
            self._recipients.append(email)

    ##############################################

    def add_recipients_from_string(self, recipients):

        self.add_recipients([x.strip() for x in recipients.split(',')])

    ##############################################

    def send(self):

        if not self._recipients:
            raise ValueError("Recipients is empty")

        message = MIMEText(self.message)
        message['Subject'] = self._subject
        message['From'] = self._from_address
        message['To'] = ', '.join([x + ' <' + x + '>' for x in self._recipients])

        smtp = smtplib.SMTP()
        smtp.connect()
        smtp.sendmail(self._from_address,
                      self._recipients,
                      message.as_string())
        smtp.quit()

####################################################################################################
#
# End
#
####################################################################################################
