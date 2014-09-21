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

class RowLayoutManager(object):

    """ This class implements a row layout manager. """

    ##############################################

    def __init__(self, grid_layout):

        self._grid_layout = grid_layout
        self.row = 0

    ##############################################

    def add_row(self, widgets):

        """ Add the widgets to the current row and go to to the next row.  If an item is :obj:`None`
        the column is skipped.
        """

        for i, widget in enumerate(widgets):
            if widget is not None:
                self._grid_layout.addWidget(widget, self.row, i)
        self.row += 1

####################################################################################################
# 
# End
# 
####################################################################################################
