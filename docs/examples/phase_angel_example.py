#Plot a graph of phase angle of planets based on time

#Import PySpace2 interface
from PySpace2 import PySpace2

#Choose how many days analysis must cover
delta_days = 1000

#Choose when to start analysis
date = {"year": 2001, "month": 9, "day": 13, "hour": 5, "minute": 0, "second": 0}

#Choose planets on the map, Currently you've got this planet available:
#["Sun, "Venus", "Earth", "Moon", "Mars", "Jupiter", "Saturn", "Uran", "Neptun"]
chosen_planets = ["Sun", "Venus", "Moon", "Mars"]

#Create phase_angel object
phase_angle = PySpace2.phase_angel()

#Show plot, plot() docstring show exactly 
#how to manipulate display format and location of saved map
phase_angle.plot()



