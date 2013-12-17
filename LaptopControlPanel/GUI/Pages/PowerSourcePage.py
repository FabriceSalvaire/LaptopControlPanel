####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import subprocess
import re
import sys

from PyQt4 import QtGui

####################################################################################################

from .Page import PageBase
from LaptopControlPanel.System.PowerSource import PowerSources
import LaptopControlPanel.Config.Config as Config

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
        self.refresh_battery_charge_threshold()

        self._init_connection()

    ##############################################

    def _init_connection(self):

        form = self._form

        form.always_charge_battery_check_box.stateChanged.connect(self._always_charge_battery_check_box_changed)
        form.apply_battery_charge_thresholds_push_button.clicked.connect(self._apply_battery_charge_thresholds)

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

    ##############################################

    def refresh_battery_charge_threshold(self):

        form = self._form

        try:
            start_threshold, stop_threshold = self._get_battery_charge_threshold()
            form = self._form
            if start_threshold == 0 and stop_threshold == 0:
                start_threshold, stop_threshold = Config.Battery.default_charge_thresholds
                always_charge_battery = True
            else:
                always_charge_battery = False
            form.charge_thresholds_group_box.setEnabled(not always_charge_battery)
            form.always_charge_battery_check_box.setChecked(always_charge_battery)
            form.start_threshold_spin_box.setValue(start_threshold)
            form.stop_threshold_spin_box.setValue(stop_threshold)
            form.error_message_label.hide()
        except:
            form.battery_charge_settings_group_box.setEnabled(False)

    ##############################################

    def _set_battery_charge_threshold(self, start_threshold, stop_threshold):

        try:
            subprocess.check_output(['battery-control', '--gui',
                                     'set-threshold', '--start=%u' %start_threshold, '--stop=%u' % stop_threshold])
        except subprocess.CalledProcessError as exception:
            raise NameError("Set threshold call failed:\n" + exception.output)

    ##############################################

    def _get_battery_charge_threshold(self):

        try:
            output = subprocess.check_output(['battery-control', '--gui', 'get-threshold'])
        except subprocess.CalledProcessError as exception:
            print exception.output
            raise NameError("Get threshold call failed:\n" + exception.output)
        # {"start_threshold": 39, "stop_threshold": 80}
        prefix = '{"start_threshold": '
        location = output.find(prefix)
        found = False
        if location != -1:
            match = re.match(r'^{"start_threshold": (\d+), "stop_threshold": (\d+)}',
                             output[location:])
            if match is not None:
                start_threshold, stop_threshold = [int(x) for x in match.groups()]
                found = True
        if not found:
            raise NameError("Couldn't found thresholds in:\n" + output)

        return start_threshold, stop_threshold

    ##############################################

    def _always_charge_battery_check_box_changed(self, state):

        self._form.charge_thresholds_group_box.setEnabled(not state)
        if state:
            self._set_battery_charge_threshold(0, 0)

    ##############################################

    def _apply_battery_charge_thresholds(self):

        start_threshold, stop_threshold = [spin_box.value() for spin_box in
                                           self._form.start_threshold_spin_box,
                                           self._form.stop_threshold_spin_box
                                           ]
        self._set_battery_charge_threshold(start_threshold, stop_threshold)

####################################################################################################
# 
# End
# 
####################################################################################################
