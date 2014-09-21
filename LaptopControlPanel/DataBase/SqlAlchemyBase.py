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
#
#                                              Audit
#
# - 04/06/2013 Fabrice
#   get_...
#
####################################################################################################

####################################################################################################

# import logging
import sqlalchemy

####################################################################################################

from PyQt4 import QtCore, QtGui

####################################################################################################

class SqlRow(object):

    ##############################################
    
    @classmethod
    def column_names(cls):

        return [column.name for column in cls.__table__.columns]

    ###############################################

    @classmethod
    def get_column(cls, column):

        return cls.__table__.columns.get(column)

    ###############################################

    @classmethod
    def get_field_title(cls, field):

        info = cls.get_column(field).info
        if 'title' in info:
            return info['title']
        else:
            return ''

    ###############################################

    @classmethod
    def get_field_witdh(cls, field):

        info = cls.get_column(field).info
        if 'width' in info:
            return info['width']
        else:
            return None

    ##############################################
    
    def get_column_dict(self):

        return {column:getattr(self, column) for column in self.column_names()}

    ##############################################
    
    def column_values(self):

        return [getattr(self, column) for column in self.column_names()]

####################################################################################################

class SqlTable(object):

    ROW_CLASS = None

    ##############################################

    def __init__(self, database):

        # Fixme: database vs session ?

        self._database = database
        self._session = database.session

    ###############################################

    def commit(self):

        self._session.commit()

    ###############################################

    def add(self, row):

        self._session.add(row)
        # self.commit()

    ###############################################

    def add_new_row(self, **kwargs):

        row = self.ROW_CLASS(**kwargs)
        self.add(row)

    ###############################################

    def query(self):

        # Close session else data are cached by the transaction ?
        # /!\ converted = True doesn't work anymore
        # self._session.close()

        return self._session.query(self.ROW_CLASS)

    ##############################################

    def all(self):

        return self.query().all()

    ###############################################

    def select_by_where_clause(self, where_clause):

        return self.query().filter(where_clause)

    ###############################################

    def select_by(self, **kwargs):

        filters = [getattr(self.ROW_CLASS, key) == value
                   for key, value in kwargs.items()]

        return self.query().filter(*filters)

    ##############################################

    def model(self):

        return SqlTableModel(self)

####################################################################################################

class ColumnWidthFactory(object):

    ##############################################

    def  __init__(self, template='M', factor=1):

        self._template = template
        self._factor = factor

    ##############################################

    def  __call__(self, font_metrics):

        return self._factor * font_metrics.width(self._template)

####################################################################################################

class ColumnDateWidthFactory(ColumnWidthFactory):

    ##############################################

    def  __init__(self, factor=1):

        super(ColumnDateWidthFactory, self).__init__(template='x7777-77-77 77:77:77x', factor=factor)

####################################################################################################

class SqlTableModel(QtCore.QAbstractTableModel):

    ##############################################

    def __init__(self, sql_table):

        super(SqlTableModel, self).__init__()

        self._sql_table = sql_table

        self._columns = self._sql_table.ROW_CLASS.column_names() # Fixme: ?
        self._rows = []
        self._query = None
        self._sort_order = None

    ##############################################

    def __getitem__(self, _slice):

        return self._rows[_slice]

    ##############################################

    def _get_row_class(self):

        return self._sql_table.ROW_CLASS

    row_class = property(_get_row_class)

    ##############################################

    def _sort(self):

        if self._query is None:
            return

        if self.sorted():
            if self._sort_order == QtCore.Qt.AscendingOrder: 
                query = self._query.order_by(self._sorted_column)
            else:
                query = self._query.order_by(sqlalchemy.desc(self._sorted_column))
        else:
            query = self._query
        self._rows = query.all()
        self.reset()

    ##############################################

    def sort(self, column_index, order):

        column_name = self._columns[column_index]
        column = self.row_class.get_column(column_name) # Fixme: ?
        self._sorted_column = column
        self._sort_order = order
        self._sort()

    ##############################################

    def sorted(self):

        return self._sort_order is not None

    ##############################################

    def data(self, index, role=QtCore.Qt.DisplayRole):

        # Fixme: why ?
        if not index.isValid():
            return QtCore.QVariant()

        if role == QtCore.Qt.DisplayRole:
            try:
                row = self._rows[index.row()]
                column = self._columns[index.column()]
            except:
                return QtCore.QVariant()
            return QtCore.QVariant(str(getattr(row, column)))

        return QtCore.QVariant ()

    ##############################################

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):

        if role == QtCore.Qt.TextAlignmentRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QVariant(int(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
            else:
                return QtCore.QVariant(int(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter))
        
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                column_name = self._columns[section]
                title = self.row_class.get_field_title(column_name) # Fixme: ?
                return QtCore.QVariant(title)
            else:
                return QtCore.QVariant(section)

        return QtCore.QVariant()

    ##############################################

    def set_column_widths(self, table_wiew):

        font_metrics = table_wiew.fontMetrics()
        for column_index, column_name in enumerate(self._columns):
            width_title = font_metrics.width('M'*2 + self.row_class.get_field_title(column_name))
            width_factory = self.row_class.get_field_witdh(column_name)
            if width_factory is not None:
                width = max(width_factory(font_metrics), width_title)
            else:
                width = width_title
            table_wiew.setColumnWidth(column_index, width)
                    
    ##############################################

    def columnCount(self, index=QtCore.QModelIndex()):

        return len(self._columns)

    ##############################################

    def rowCount(self, index=QtCore.QModelIndex()):

        return len(self._rows)

    ##############################################

    def column_index(self, column):

        return self._columns.index(column)

    ##############################################

    def all(self):

        self._query = self._sql_table.query()
        self._sort()

    ##############################################

    def select_by(self, **kwargs):

        self._query = self._sql_table.select_by(**kwargs)
        self._sort()

    ##############################################

    def select_by_where_clause(self, where_clause):

        self._query = self._sql_table.select_by_where_clause(where_clause)
        self._sort()

####################################################################################################
# 
# End
# 
####################################################################################################
