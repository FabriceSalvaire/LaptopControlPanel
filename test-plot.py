#! /usrb/bin/env ipython --pylab=qt

from pylab import *
from LaptopControlPanel.Monitoring.BatteryStatusDataBase import BatteryStatusDataBase

db = BatteryStatusDataBase('battery-status.sqlite')
data = db.battery_status_table.to_array()

# 1371026025.72309,60,51,0.06,0.13,0.16
data = data.transpose()
data[0] -= data[0,0]
print data

fig = figure()
plot(data[0], data[2])
show()

# End

