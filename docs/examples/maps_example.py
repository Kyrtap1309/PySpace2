#Planets' Map at Equatorial Coordinate System

#Import PySpace2 interface
from PySpace2 import PySpace2

#Choose when to start analysis
date = {"year": 2001, "month": 9, "day": 13, "hour": 5, "minute": 0, "second": 0}

#Choose planets on the map, Currently you've got this planet available:
#["Sun, "Venus", "Earth", "Moon", "Mars", "Jupiter", "Saturn", "Uran", "Neptun"]
chosen_planets = ["Sun", "Venus", "Moon", "Mars"]

#Create Map object
map = PySpace2.map(date=date, chosen_planets=chosen_planets)

#Show map, plot_map() docstring show exactly 
#how to manipulate display format and location of saved map
map.plot_map()



