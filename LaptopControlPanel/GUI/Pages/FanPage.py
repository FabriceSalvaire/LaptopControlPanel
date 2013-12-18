# -*- coding: utf-8 -*-

####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

from .Page import PageBase
from LaptopControlPanel.Acpi.Fan import FanManager
from LaptopControlPanel.System.Hdd import HddManager

####################################################################################################

from .ui.FanPage_ui import Ui_form

####################################################################################################

class FanPage(PageBase):

    __page_name__ = 'fan'
    __page_title__ = 'FAN'

    ##############################################

    def __init__(self, parent=None):

        super(FanPage, self).__init__(parent)

        self._form = Ui_form()
        self._form.setupUi(self)

        for widget in (self._form.fan_level_spin_box,
                       self._form.fan_level_slider,
                       ):
            widget.setMinimum(1)
            widget.setMaximum(7)
            widget.setSingleStep(1)
            # widget.setPageStep(1)

        self._hdd_manager = HddManager()
        self._fan_manager = FanManager()
        self.refresh()

        self._init_connection()

    ##############################################

    def _init_connection(self):

        form = self._form

        form.fan_level_spin_box.valueChanged.connect(self._on_fan_level_change)
        form.auto_radio_button.toggled.connect(self._on_fan_level_change)
        form.disengaged_radio_button.toggled.connect(self._on_fan_level_change)
        form.full_speed_radio_button.toggled.connect(self._on_fan_level_change)

    ##############################################

    def refresh(self, refresh_level=True):

        form = self._form

        form.hdd_temperature_label.setText(str(self._hdd_manager.temperature()) + u' °C')
        form.fan_speed_label.setText(str(self._fan_manager.speed) + ' rpm')
      
        if refresh_level:
            level = self._fan_manager.level
            try:
                level = int(level)
                form.fan_level_spin_box.setValue(level)
                form.level_radio_button.setChecked(True)
            except:
                if level == 'auto':
                    form.auto_radio_button.setChecked(True)
                elif level == 'disengaged':
                    form.disengaged_radio_button.setChecked(True)
                elif level == 'full-speed':
                    form.full_speed_radio_button(True)

    ##############################################

    def _on_fan_level_change(self):

        form = self._form

        if form.level_radio_button.isChecked():
            level = form.fan_level_spin_box.value()
        elif form.auto_radio_button.isChecked():
            level = 'auto'
        elif form.disengaged_radio_button.isChecked():
            level = 'disengaged'
        elif form.full_speed_radio_button.isChecked():
            level = 'full-speed'
        # if level == 8:
        #     level = 'full-speed'
        self._fan_manager.level = level
        self.refresh(refresh_level=False)

####################################################################################################
# 
# End
# 
####################################################################################################
