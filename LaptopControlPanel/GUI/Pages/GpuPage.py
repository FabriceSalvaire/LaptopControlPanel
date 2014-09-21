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

from .Page import PageBase
from LaptopControlPanel.Acpi.Gpu import GpuManager

####################################################################################################

from .ui.GpuPage_ui import Ui_form

####################################################################################################

class GpuPage(PageBase):

    __page_name__ = 'gpu'
    __page_title__ = 'GPU'

    ##############################################

    def __init__(self, parent=None):

        super(GpuPage, self).__init__(parent)

        self._form = Ui_form()
        self._form.setupUi(self)

        self.refresh()

        self._init_connection()

    ##############################################

    def _init_connection(self):

        if GpuManager.has_bbswitch():
            self._form.on_off_button.clicked.connect(self._change_gpu_state)

    ##############################################

    def _set_on_off_label(self):

        label = 'ON' if self._gpu_state else 'OFF'
        self._form.on_off_button.setText(label)

    ##############################################

    def _change_gpu_state(self):

        self._gpu_state = not self._gpu_state
        GpuManager.set_state(self._gpu_state)
        gpu_state = GpuManager.state()
        if gpu_state == self._gpu_state:
            self._set_on_off_label()
        else:
            raise NameError('Gpu refuse to change of state')

    ##############################################

    def refresh(self):

        if GpuManager.has_bbswitch():
            self._gpu_state = GpuManager.state()
        else:
            self._gpu_state = False
        self._set_on_off_label()

####################################################################################################
# 
# End
# 
####################################################################################################
