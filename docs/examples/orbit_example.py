#Show orbit of some celestial body in Solar System

#Import PySpace2 interface
from PySpace2 import PySpace2

#Choose when to start analysis
date = {"year": 2001, "month": 9, "day": 13, "hour": 5, "minute": 0, "second": 0}

#Choose planet, which parameters of orbit you want to show
#Available planets: ["Venus", "Earth", "Moon", "Mars", "Jupiter", "Saturn", "Uran", "Neptun", "Ceres"]
planet = "ceres" #You can type planet name in any case. Capitalization doesn't matter

#Create Orbit object
orbit = PySpace2.orbit(date=date, chosen_planets=planet)

#Print parameters of orbit (Recommended way is to storage them in pandas DataFrame)
data = orbit.show_params()




