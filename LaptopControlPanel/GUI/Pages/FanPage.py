# -*- coding: utf-8 -*-

####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import logging

from PyQt4 import QtCore, QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np

####################################################################################################

from .Page import PageBase
from LaptopControlPanel.Acpi.Fan import FanManager
from LaptopControlPanel.Monitoring.RoundRobinMonitoring import RoundRobinMonitoring, DataProvider
from LaptopControlPanel.System.Hdd import HddManager

####################################################################################################

from .ui.FanPage_ui import Ui_form

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class HddTemperatureDataProvider(DataProvider):

    __name__ = 'HDD Temperature'
    __dtype__ = np.uint

    ##############################################

    def __init__(self):
        self._hdd_manager = HddManager()

    ##############################################

    def __call__(self):
        return self._hdd_manager.temperature()

####################################################################################################

class FanSpeedDataProvider(DataProvider):

    __name__ = 'Fan Speed'
    __dtype__ = np.uint

    ##############################################

    def __init__(self):
        self._fan_manager = FanManager()

    ##############################################

    def __call__(self):
        return self._fan_manager.speed

####################################################################################################

class FanPage(PageBase):

    __page_name__ = 'fan'
    __page_title__ = 'FAN'

    _logger = _module_logger.getChild('FanPage')

    ##############################################

    def __init__(self, parent=None):

        super(FanPage, self).__init__(parent)

        self._form = Ui_form()
        self._form.setupUi(self)

        self._hdd_manager = HddManager()
        self._fan_manager = FanManager()

        self._monitoring = None

        self._init_ui()
        self._init_connection()
        self.refresh()

    ##############################################

    def _init_ui(self):

        form = self._form

        for widget in (form.fan_level_spin_box,
                       form.fan_level_slider,
                       ):
            widget.setMinimum(1)
            widget.setMaximum(7)
            widget.setSingleStep(1)
            # widget.setPageStep(1)

        self._figure = Figure()
        self._axes_left = self._figure.add_subplot(1, 1, 1)
        self._axes_right = self._axes_left.twinx()


        self._canvas = FigureCanvas(self._figure)
        self._canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        self._canvas.setFocus()

        self._matplotlib_toolbar = NavigationToolbar(self._canvas, self)

        for widget in self._canvas, self._matplotlib_toolbar:
             form.graphic_layout.addWidget(widget)

    ##############################################

    def _init_connection(self):

        form = self._form

        form.fan_level_spin_box.valueChanged.connect(self._on_fan_level_change)
        form.auto_radio_button.toggled.connect(self._on_fan_level_change)
        form.disengaged_radio_button.toggled.connect(self._on_fan_level_change)
        form.full_speed_radio_button.toggled.connect(self._on_fan_level_change)
        form.monitor_check_box.stateChanged.connect(self._on_monitor_state_changed)

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
                    form.full_speed_radio_button.setChecked(True)

        if self._monitoring is not None and self._monitoring.data_frame:
            self._logger.info("Refresh plot")

            time_slot = self._monitoring.time_slot

            axes = self._axes_left
            axes.clear()        
            axes.grid(True)
            # times = np.arange(self._monitoring.period)
            times = np.arange(time_slot)
            axes.set_xlabel('Times')

            data_provider_name = 'Fan Speed'
            axes.plot(times, self._monitoring.data_frame[data_provider_name][:time_slot], 'green')
            axes.set_ylabel(data_provider_name)
            axes.set_ylim(0, 6000)
            # self._figure.add_axes(self._monitoring._data_frame.plot()) # segfault

            data_provider_name = 'HDD Temperature'
            axes = self._axes_right
            axes.clear()        
            axes.set_ylabel(data_provider_name)
            axes.set_ylim(0, 60)
            axes.plot(times, self._monitoring.data_frame[data_provider_name][:time_slot], 'red')

            self._canvas.draw()

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

    ##############################################

    def _on_monitor_state_changed(self, state):

        if state:
            data_providers = (HddTemperatureDataProvider, FanSpeedDataProvider)
            self._monitoring = RoundRobinMonitoring(time_resolution=20, #s
                                                    time_period=500,
                                                    data_providers=data_providers)
            self._monitoring.start()
            # self.refresh()
        else:
            if self._monitoring:
                self._monitoring.stop()
                self._monitoring = None

####################################################################################################
# 
# End
# 
####################################################################################################
