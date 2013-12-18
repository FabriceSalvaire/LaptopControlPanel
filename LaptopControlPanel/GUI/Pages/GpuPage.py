####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
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

        self._gpu_state = GpuManager.state()
        self._set_on_off_label()

####################################################################################################
# 
# End
# 
####################################################################################################
