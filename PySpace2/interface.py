import os

import spiceypy
from spiceypy.utils.exceptions import SpiceNOSUCHFILE

from .utilities.kernels_utilities import download_file
from .utilities.kernels_constants import KERNELS_URLS
from .utilities.kernels_constants import REQUIRED_FILES

class PySpace2:

    @classmethod
    def _handle_spice_exception(cls, method_name):
        required_files = REQUIRED_FILES.get(method_name, [])
        print(f"Method '{method_name}' failed due to missing kernel files.")
        print(
            f"Please download the following required files: {', '.join(required_files)}"
        )

    def download_kernels(self, method_name):
        for file in REQUIRED_FILES[method_name]:
            naif_relative_path = KERNELS_URLS[file]
            local_relative_path = "../kernels/" + os.path.dirname(file)
            download_file(naif_relative_path, local_relative_path)
            

    @staticmethod
    def earth():
        """
        Make Earth object
        """
        try:
            from .planets.earth import Earth

            return Earth()
        except SpiceNOSUCHFILE:
            PySpace2._handle_spice_exception("earth")

    @staticmethod
    def first_kepler(delta_days: int, date: dict):
        """
        Make FirstKepler object

        Parameters:
        -----------
        delta_days : int
            Number of days to compute the trajectory for.
        date : dict
            Starting date for the computation (year, month, day, hour, minute, second).
        """
        try:
            from .planets.first_kepler import FirstKepler

            return FirstKepler(delta_days, date)
        except SpiceNOSUCHFILE:
            PySpace2._handle_spice_exception("first_kepler")

    @staticmethod
    def solar_system(delta_days: int, date: dict):
        """
        Create SolarSystem object

        Parameters:
        -----------
        delta_days : int
            Number of days to compute the trajectory for.
        date : dict
            Starting date for the computation (year, month, day, hour, minute, second).
        """
        try:
            from .planets.solar_system import SolarSystem

            return SolarSystem(delta_days, date)
        except SpiceNOSUCHFILE:
            PySpace2._handle_spice_exception("solar_system")

    @staticmethod
    def phase_angel(delta_days: int, date: dict, chosen_planets: list):
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
        try:
            from .planets.phase_angel import PhaseAngle

            return PhaseAngle(delta_days, date, chosen_planets)
        except SpiceNOSUCHFILE:
            PySpace2._handle_spice_exception("phase_angel")

    @staticmethod
    def venus(begin_date: dict, end_date: dict):
        """Create a Venus object

        Parameters:
        -----------
        begin_date : dict
            begin date when to start making calculations for Venus

        end_date : dict
            end date when to stop making calculations for Venus

        """
        try:
            from .planets.venus import Venus

            return Venus(begin_date, end_date)
        except SpiceNOSUCHFILE:
            PySpace2._handle_spice_exception("venus")

    @staticmethod
    def map(date: dict, chosen_planets: list[str]):
        """Create a Map object

        Parameters:
        -----------
        date: dict
            Day to project planets location on the map

        chosen_planets: list[str]
            Planets which locations will be projected on the map
        """
        try:
            from .planets.maps import Map

            return Map(date, chosen_planets)
        except SpiceNOSUCHFILE:
            PySpace2._handle_spice_exception("map")

    @staticmethod
    def orbit(date: dict, chosen_planet: str):
        """Create a Orbit object

        Parameters:
        -----------
        date : dict
            Day to calculate planet's orbit parameters
        chosen_planet : str
            Chosen planet for the calculations
        """
        try:
            from .planets.orbit import Orbit

            return Orbit(date, chosen_planet)
        except SpiceNOSUCHFILE:
            PySpace2._handle_spice_exception("orbit")
