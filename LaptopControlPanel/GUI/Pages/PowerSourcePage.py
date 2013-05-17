####################################################################################################
# 
# @Project@ - @ProjectDescription@.
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

from PyQt4 import QtGui

####################################################################################################

from .Page import PageBase
from LaptopControlPanel.System.PowerSource import PowerSources

####################################################################################################

from .ui.PowerSourcePage_ui import Ui_form

####################################################################################################

class PowerSourcePage(PageBase):

    __page_name__ = 'power_source'
    __page_title__ = 'Power Source'

    ##############################################

    def __init__(self, parent=None):

        super(PowerSourcePage, self).__init__(parent)

        self._form = Ui_form()
        self._form.setupUi(self)

        self._power_sources = PowerSources()

        self.refresh()

    ##############################################

    def refresh(self):

        form = self._form

        ac = self._power_sources['AC']
        if ac.online:
            ac_status = 'online'
        else:
            ac_status = 'offline'
        form.ac_status_label.setText(ac_status)

        battery = self._power_sources['BAT0']
        form.battery_status_label.setText(battery.status)
        form.battery_capacity_label.setText('%u %%' % battery.capacity)
        form.battery_cycle_count_label.setText(str(battery.cycle_count))

####################################################################################################
# 
# End
# 
####################################################################################################
