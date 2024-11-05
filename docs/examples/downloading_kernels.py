#There may be a situation in which PySpace2 returns an error about missing kernels. 
#This is a rare situation, but PySpace2 has an internal mechanism that allows for fixing this error

#Import PySpace2 Interface
from PySpace2 import PySpace2

#Make the PySpace2 object
space = PySpace2()

#Install missing kernels (download_kernels function needs API method as an argument)
space.download_kernels("earth")

