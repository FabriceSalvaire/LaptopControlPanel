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

""" This module provides an interface to ACPI Calls to control Thinkpad Laptop Battery.

These ACPI calls permits:
* to set the start and stop capacity threshold to charge the battery,
* to switch on battery when AC power is plugged,
* to setup a "peak shift" procedure.

(As far I know) The concept of "peak shift" is to switch temporarily electrical devices on battery
during a power peak consumption period so as to unload the grid.  This power management strategy is
relevant for country like Japan, where these peak periods represent a risk of electrical black out.
"""

####################################################################################################

from LaptopControlPanel.Acpi.AcpiCall import AcpiCallDevice, AcpiCallArguments

####################################################################################################

class BatteryControl(object):

    # LPC means Low Pin Count Bus
    # EC means Embedded Controller
    _asl_base = r'\_SB.PCI0.LPC.EC.HKEY'

    either_both_battery, main_battery, secondary_battery = range(3)

    ##############################################

    def __init__(self):

        self._acpi_call_device = AcpiCallDevice()

        # Peak Shift State

        self._get_peak_shift_state_acpi_call = self._define_function(
            name='PSSG',
            input_arguments=AcpiCallArguments(reserved=31),
            output_arguments=AcpiCallArguments(inhibit_charge_status=0,
                                               reserved1=3,
                                               discharge_with_ac_capability=4,
                                               inhibit_charge_capability=5,
                                               inhibit_charge_auto_reset_capability=6,
                                               reserved2=7,
                                               inhibit_charge_effective_timer=23,
                                               reserved3=30,
                                               error_status=31,
                                               ),
            )

        self._set_peak_shift_state_acpi_call = self._define_function(
            name='PSSS',
            input_arguments=AcpiCallArguments(inhibit_charge=0,
                                              reserved1=7,
                                              timer=23,
                                              reserved2=31,
                                              ),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )

        self._set_peak_shift_discharge_state_acpi_call = self._define_function(
            name='PSBS',
            input_arguments=AcpiCallArguments(battery_id=7,
                                              discharge_status=15,
                                              reserved=31),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )

        # Inhibit Charge
        
        self._set_inhibit_charge_state_acpi_call = self._define_function(
            name='BICS',
            input_arguments=AcpiCallArguments(inhibit_charge=0,
                                              reserved1=3,
                                              battery_id=5,
                                              reserved2=7,
                                              timer=23,
                                              reserved3=31,
                                              ),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )

        # Battery Charge Start Threshold

        self._get_charge_start_threshold_acpi_call = self._define_function(
            name='BCTG',
            input_arguments=AcpiCallArguments(battery_id=7,
                                              reserved=31,
                                              ),
            output_arguments=AcpiCallArguments(start_threshold=7,
                                               capability=8,
                                               can_specify_every_battery=9,
                                               reserved=30,
                                               error_status=31,
                                               ),
            )

        self._set_charge_start_threshold_acpi_call = self._define_function(
            name='BCCS',
            input_arguments=AcpiCallArguments(start_threshold=7,
                                              battery_id=9,
                                              reserved=31,
                                              ),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )

        # Battery Charge Stop Threshold
        
        self._get_charge_stop_threshold_acpi_call = self._define_function(
            name='BCSG',
            input_arguments=AcpiCallArguments(battery_id=7,
                                              reserved=31),
            output_arguments=AcpiCallArguments(stop_threshold=7,
                                               capability=8,
                                               can_specify_every_battery=9,
                                               reserved=30,
                                               error_status=31,
                                               ),
            )

        self._set_charge_stop_threshold_acpi_call = self._define_function(
            name='BCSS',
            input_arguments=AcpiCallArguments(stop_threshold=7,
                                              battery_id=9,
                                              reserved=31,
                                              ),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )

        # Battery Discharge State

        self._get_discharge_state_acpi_call = self._define_function(
            name='BDSG',
            input_arguments=AcpiCallArguments(battery_id=7,
                                              reserved=31),
            output_arguments=AcpiCallArguments(discharge_status=0,
                                               break_by_ac_detaching=1,
                                               reserved1=7,
                                               discharge_capability=8,
                                               can_specify_every_battery=9,
                                               can_break=10,
                                               reserved2=30,
                                               error_status=31,
                                               ),
            )

        self._set_discharge_state_acpi_call = self._define_function(
            name='BDSS',
            input_arguments=AcpiCallArguments(force_discharge=0,
                                              break_by_ac_detaching=1,
                                              reserved1=7,
                                              battery_id=9,
                                              reserved2=31),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )

    ##############################################

    def _define_function(self, name, input_arguments, output_arguments):

        return self._acpi_call_device.define_function(self._asl_base + '.' + name,
                                                      input_arguments, output_arguments)

    ##############################################

    def _check_battery_id_for_reading(self, battery):

        if battery == self.either_both_battery:
            raise ValueError("Can't specify either or both battery for reading.")

    ##############################################

    def _check_charge_threshold(self, threshold=None):

        if threshold is None:
            threshold = 0
        elif not (0 <= threshold <= 99):
            raise ValueError("Wrong charge threshold value " + str(threshold))
        return str(threshold)

    ##############################################

    def _check_error_status(self, result):

        if result.error_status:
            raise ValueError("ACPI call failed")

    ##############################################

    def set_start_threshold(self, battery=main_battery, threshold=None):

        threshold = self._check_charge_threshold(threshold)
        result = self._set_charge_start_threshold_acpi_call.call(battery_id=battery,
                                                                 start_threshold=threshold,
                                                                 )
        self._check_error_status(result)

    ##############################################

    def set_stop_threshold(self, battery=main_battery, threshold=None):

        threshold = self._check_charge_threshold(threshold)
        result = self._set_charge_stop_threshold_acpi_call.call(battery_id=battery,
                                                                stop_threshold=threshold,
                                                                )
        self._check_error_status(result)

    ##############################################

    def get_start_threshold(self, battery=main_battery):
        self._check_battery_id_for_reading(battery)
        return self._get_charge_start_threshold_acpi_call.call(battery_id=battery)

    ##############################################

    def get_stop_threshold(self, battery=main_battery):
        self._check_battery_id_for_reading(battery)
        return self._get_charge_stop_threshold_acpi_call.call(battery_id=battery)
    
    ##############################################

    def get_inhibit_charge(self):
        call = 'BICS'

    def set_inhibit_charge(self, value):
        call = 'BICG'        

    ##############################################

    def set_force_discharge(self, battery=main_battery, force_discharge=True, break_by_ac_detaching=False):
        result = self._set_discharge_state_acpi_call.call(battery_id=battery,
                                                          force_discharge=force_discharge,
                                                          break_by_ac_detaching=break_by_ac_detaching,
                                                          )
        self._check_error_status(result)

    ##############################################       

    def get_force_discharge(self, battery=main_battery):
        self._check_battery_id_for_reading(battery)
        return self._get_discharge_state_acpi_call.call(battery_id=battery)

    ##############################################

    def set_peak_shift_state(self):
        call = 'PSSS'

    def get_peak_shift_state(self):
        return self._get_peak_shift_state_acpi_call.call()

####################################################################################################
# 
# End
# 
####################################################################################################
