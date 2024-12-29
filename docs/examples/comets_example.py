#Comets class functionalities

#Import PySpace2 interface
from PySpace2 import PySpace2

#Make comets object
comets = PySpace2.comets()

#Get statistics of P type comets and C type comets
print(comets.description("P"))
print(comets.description("C"))

#Plots the inclination vs aphelion of comets with bound orbits
comets.plot_inc_vs_aph() 
