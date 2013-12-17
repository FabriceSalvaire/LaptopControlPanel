####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

from datetime import datetime
import time

####################################################################################################

from sqlalchemy import Column, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base

####################################################################################################

SqlAlchemyBase = declarative_base()

####################################################################################################

from LaptopControlPanel.DataBase.SqlAlchemyBase import (SqlRow, SqlTable)
from LaptopControlPanel.DataBase.SqliteDataBase import SqliteDataBase
from LaptopControlPanel.Tools.DictionaryTools import init_default_key

####################################################################################################

class BatteryStatusRow(SqlAlchemyBase, SqlRow):

    __tablename__ = 'battery_status'

    # date = Column(Date, primary_key=True)
    date = Column(Float, primary_key=True)
    time_resolution = Column(Integer, nullable=False)
    battery_capacity = Column(Integer, nullable=False)
    load_average_1_min = Column(Float, nullable=False)
    load_average_5_min = Column(Float, nullable=False)
    load_average_15_min = Column(Float, nullable=False)

    ##############################################
        
    def __repr__(self):
        
        message = '''
Battery Status Row
  date: %(date)s
  time resolution: %(time_resolution)u s
  battery capacity: %(battery_capacity)s
  load average 1 min: %(load_average_1_min)s
               5 min: %(load_average_5_min)s
              15 min: %(load_average_15_min)s
'''
        return message % self.get_column_dict()

####################################################################################################

class BatteryStatusSqlTable(SqlTable):

    ROW_CLASS = BatteryStatusRow

    ##############################################

    def add_new_row(self, **kwargs):
    
        init_default_key(kwargs,
                         # date=datetime.today(),
                         date=time.time(),
                         )

        super(BatteryStatusSqlTable, self).add_new_row(**kwargs)
        self.commit()

    ##############################################

    def to_array(self):

        import numpy as np

        column_names = self.ROW_CLASS.column_names()
        query = self.query()
        array = np.zeros((query.count(), len(column_names)), dtype=np.float)
        r = 0
        for row in query:
            array[r] = row.column_values()
            r += 1

        return array

####################################################################################################

class BatteryStatusDataBase(SqliteDataBase):
    
    __base__ = SqlAlchemyBase

    ##############################################
    
    def __init__(self, filename, echo=False):

        super(BatteryStatusDataBase, self).__init__(filename, echo)

        self.battery_status_table = BatteryStatusSqlTable(self)

####################################################################################################
# 
# End
# 
####################################################################################################
