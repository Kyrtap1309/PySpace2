from .planets.earth import Earth
from .planets.first_kepler import FirstKepler
from .planets.solar_system import SolarSystem
from .planets.phase_angel import PhaseAngle
from .planets.venus import Venus
from .planets.maps import Map


class PySpace2:

    @staticmethod
    def earth() -> Earth:
        """
        Make Earth object
        """
        earth = Earth()
        return earth
    
    @staticmethod
    def first_kepler(delta_days: int, date: dict) -> FirstKepler:
        """
        Make FirstKepler object
        
        Parameters:
        -----------
        delta_days : int
            Number of days to compute the trajectory for.
        date : dict
            Starting date for the computation (year, month, day, hour, minute, second).
        """
        first_kepler = FirstKepler(delta_days, date)
        return first_kepler
    
    @staticmethod
    def solar_system(delta_days: int, date: dict) -> SolarSystem:

        """
        Create SolarSystem object

        Parameters:
        -----------
        delta_days : int
            Number of days to compute the trajectory for.
        date : dict
            Starting date for the computation (year, month, day, hour, minute, second).
        """
        
        solar_system = SolarSystem(delta_days, date)
        return solar_system
    
    @staticmethod
    def phase_angel(delta_days: int, date: dict, chosen_planets: list) -> PhaseAngle:
        """
        Create PhaseAngel object

        Parameters:
        -----------
        delta_days : int
            Number of days to compute the trajectory for.
        date : dict
            Starting date for the computation (year, month, day, hour, minute, second).
        chosen_planets: list
            List of planets, which plots are supposed to be generated
        """
        phase_angle = PhaseAngle(delta_days, date, chosen_planets)
        return phase_angle

    @staticmethod
    def venus(begin_date: dict, end_date: dict) -> Venus:
        """Create a Venus object
        
        Parameters:
        -----------
        begin_date : dict
            begin date when to start making calculations for Venus
        
        end_date : dict
            end date when to stop making calculations for Venus

        """
        
        venus = Venus(begin_date, end_date)
        return venus

    @staticmethod
    def map(date: dict, chosen_planets: list[str]) -> Map:
        """Create a Venus object
        
        Parameters:
        -----------
        date: dict
            Day to project planets location on the map
    
        chosen_planets: list[str]
            Planets which locations will be projected on the map
        """

        map = Map(date, chosen_planets)
        return map
