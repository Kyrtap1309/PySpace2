#Solar System Barycentre calculation with relation to the Sun

#Import PySpace2 interface
from PySpace2 import PySpace2


#Choose when to start analysis
date = {"year": 2001, "month": 9, "day": 13, "hour": 5, "minute": 0, "second": 0}

#Choose how many days analysis must cover
delta_days = 1000

#Make Solar System barycentre  object
first_kepler = PySpace2.first_kepler(delta_days, date)

#Solar System Barycentre info
print(first_kepler)

#Get array with Solar System Barycentre data
ssb_data_array = first_kepler.solar_system_barycentre_pos_array

#Show SSB trajectory, trajectory docstring show exactly 
#how to manipulate display format and location of saved trajectory
first_kepler.trajectory()