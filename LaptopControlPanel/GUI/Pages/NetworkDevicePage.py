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

####################################################################################################

from PyQt4 import QtCore, QtGui

####################################################################################################

from .Page import PageBase
from LaptopControlPanel.System.NetworkDevice import NetworkDevices

####################################################################################################

from .ui.NetworkDevicePage_ui import Ui_form
from LaptopControlPanel.GUI.Widgets.RowLayoutManager import RowLayoutManager

####################################################################################################

class NetworkDevicePage(PageBase):

    __page_name__ = 'network_device'
    __page_title__ = 'Network device'

    ##############################################

    def __init__(self, parent=None):

        super(NetworkDevicePage, self).__init__(parent)

        self._form = Ui_form()
        self._form.setupUi(self)

        self._network_devices = NetworkDevices()

        self.refresh()

    ##############################################

    def refresh(self):

        form = self._form

        row_layout_manager = RowLayoutManager(form.grid_layout)
        # Fixme: clear layout

        for device in self._network_devices.itervalues():
            type_label = QtGui.QLabel(device.type.title(), self)
            name_label = QtGui.QLabel(device.name, self)
            widgets = [type_label, name_label]
            if device.hard:
                hard_lock_label = QtGui.QLabel(self)
                icon = self._application.icon_loader.get_icon('object-locked', icon_size=32)
                # hard_lock_label.setText('hard locked')
                hard_lock_label.setPixmap(icon.pixmap(icon.availableSizes()[0]))
                widgets.append(hard_lock_label)
            else:
                soft_lock_check_box = QtGui.QCheckBox(self)
                soft_lock_check_box.setObjectName(device.name + '.soft_lock_check_box')
                soft_lock_check_box.setChecked(not device.soft)
                soft_lock_check_box.stateChanged.connect(self._soft_lock_state_changed)
                widgets.append(soft_lock_check_box)
            row_layout_manager.add_row(widgets)

    ##############################################

    def _soft_lock_state_changed(self, status):

        sender = self.sender()
        device_name = str(sender.objectName()).split('.')[0]
        device = self._network_devices[device_name]
        device.soft = not (status == QtCore.Qt.Checked)

####################################################################################################
# 
# End
# 
####################################################################################################
