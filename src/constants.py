#Module with all universal constants needed to calculations
import datetime
import spiceypy


spiceypy.furnsh('kernels/lsk/naif0012.tls')

#Today date (at midnight) in Year - month - dayT00:00:00 format
TODAY_DATE = datetime.datetime.today().strftime('%Y-%m-%dT00:00:00')


##Today Date as ephemeris time (ET)
ET_TODAY_DATE_MIDNIGHT = spiceypy.utc2et(TODAY_DATE)
