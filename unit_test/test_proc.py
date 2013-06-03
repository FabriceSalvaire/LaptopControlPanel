from LaptopControlPanel.System.Proc import LoadAverage

load_average = LoadAverage()
load_average.update()
print load_average.number_of_job_1_min

# End
