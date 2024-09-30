import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import spiceypy

from ..utilities.utilities import (
    get_utc_time,
    prepare_dict,
    kernels_load,
    show_or_save_fig,
)
from ..utilities.constants import NAIF_PLANETS_ID, PLANETS_COLOR, PLANETS_SIZE


class Map:
    """Class represents planets coordinates at ecliptic coordinates and equatorial coordinates"""

    def __init__(self, date: dict, chosen_planets: list[str]) -> None:
        """
        Initialize the class with date on which class calculates coordinate and with planets which coords will be calculated.

        Parameters:
        -----------
        date : dict
            Starting date for the computation (year, month, day, hour, minute, second).

        chosen_planets : dict
            Dict of planets to analyse with NAIF IDs as values

        """

        kernels = ["../kernels/spk/de432s.bsp", "../kernels/lsk/naif0012.tls"]
        kernels_load(kernels)

        self.chosen_planets = chosen_planets

        self._init_map(date, chosen_planets)
        self._init_ecliptic()

    def _init_map(self, date: dict, chosen_planets: list) -> None:
        """
        Initialize longtitudes and latitudes of chosen planets.

        Parameters:
        -----------
        date : dict
            Starting date for the computation (year, month, day, hour, minute, second).

        chosen_planets : dict
            Dict of planets to analyse with NAIF IDs as values

        """
        # Initialization of UTC time
        self._utc_time_str = get_utc_time(date).strftime("%Y-%m-%dT%H:%M:%S")
        # Initialization of ET time
        self._et_time = spiceypy.utc2et(self._utc_time_str)

        # Creating a pandas dataframe to store calculations and parameters
        self._map_dataframe = pd.DataFrame()

        # Column with UTC and ET time
        self._map_dataframe.loc[:, "ET"] = [self._et_time]
        self._map_dataframe.loc[:, "UTC"] = [self._utc_time_str]

        self._naif_chosen_planets = prepare_dict(NAIF_PLANETS_ID, chosen_planets)

        for planet_name in self._naif_chosen_planets.keys():
            # Calculation of earth - planet vector coordinates
            self._map_dataframe.loc[
                :, f"{planet_name}-earth_vector"
            ] = self._map_dataframe["ET"].apply(
                lambda x: spiceypy.spkezp(
                    targ=NAIF_PLANETS_ID[planet_name],
                    et=x,
                    ref="J2000",
                    abcorr="LT+S",
                    obs=399,
                )[0]
            )

            # Calculation of longtitude and latitude in relation to ECLIPJ2000
            # of planet
            self._map_dataframe.loc[:, f"{planet_name}_longtitude"] = (
                self._map_dataframe[f"{planet_name}-earth_vector"].apply(
                    lambda x: spiceypy.recrad(x)[1]
                )
            )

            self._map_dataframe.loc[:, f"{planet_name}_latitude"] = self._map_dataframe[
                f"{planet_name}-earth_vector"
            ].apply(lambda x: spiceypy.recrad(x)[2])

            # Convertion of longtitude angles to be able to plot them
            # in matplotlib - range from 0 to 2pi rads must be convert from -90
            # to 90 degrees

            self._map_dataframe.loc[:, f"{planet_name}_longtitude_plt"] = (
                self._map_dataframe[f"{planet_name}_longtitude"].apply(
                    lambda x: -1 * ((x % np.pi) - np.pi) if x > np.pi else -1 * x
                )
            )

    def _init_ecliptic(self) -> None:
        """
        Calculate Ecliptic and Equator coordinates.

        """

        # Creating a pandas dataframe to store calculations and parameters
        self._ecliptic_dataframe = pd.DataFrame()

        # Ecliptic longs and lats coordinates (we will calculate vector of ecliptic plane
        # for constant latitude)
        self._ecliptic_dataframe.loc[:, "Ecliptic_longtitudes"] = np.linspace(
            0, 2 * np.pi, 200
        )

        self._ecliptic_dataframe.loc[:, "Ecliptic_latitudes"] = np.pi / 2.0

        self._ecliptic_dataframe.loc[:, "Ecliptic_direction"] = (
            self._ecliptic_dataframe.apply(
                lambda x: spiceypy.sphrec(
                    r=1, colat=x["Ecliptic_latitudes"], lon=x["Ecliptic_longtitudes"]
                ),
                axis=1,
            )
        )

        # Transformation from ecliptic to equator coordinates
        _ecl_to_equ = spiceypy.pxform(
            fromstr="ECLIPJ2000", tostr="J2000", et=self._et_time
        )

        self._ecliptic_dataframe.loc[:, "Equator_direction"] = self._ecliptic_dataframe[
            "Ecliptic_direction"
        ].apply(lambda x: _ecl_to_equ.dot(x))

        self._ecliptic_dataframe.loc[:, "Equator_long"] = self._ecliptic_dataframe[
            "Equator_direction"
        ].apply(lambda x: spiceypy.recrad(x)[1])

        self._ecliptic_dataframe.loc[:, "Equator_long_plt"] = self._ecliptic_dataframe[
            "Equator_long"
        ].apply(lambda x: -1 * ((x % np.pi) - np.pi) if x > np.pi else -1 * x)

        self._ecliptic_dataframe.loc[:, "Equator_lat"] = self._ecliptic_dataframe[
            "Equator_direction"
        ].apply(lambda x: spiceypy.recrad(x)[2])

    def plot_map(
        self,
        save_fig: bool = True,
        dpi: str = 500,
        fig_name: str = "space_map.png",
        dir: str = "./plots",
    ) -> None:
        """
        Plots the map of the Equatorial Coordinate System

        """

        plt.style.use("dark_background")

        plt.figure(figsize=(12, 8))

        plt.subplot(projection="aitoff")

        plt.title(f"{self._utc_time_str}")

        for planet_name in self.chosen_planets:
            plt.plot(
                self._map_dataframe[f"{planet_name}_longtitude_plt"],
                self._map_dataframe[f"{planet_name}_latitude"],
                color=PLANETS_COLOR[planet_name],
                marker="o",
                markersize=PLANETS_SIZE[planet_name],
                label=planet_name.capitalize(),
                linestyle="None",
            )

        plt.plot(
            self._ecliptic_dataframe["Equator_long_plt"],
            self._ecliptic_dataframe["Equator_lat"],
            linestyle="None",
            marker="_",
            markersize=2,
            label="Ecliptic",
            color="tab:red",
        )

        plt.xlabel("Longtitude")
        plt.ylabel("Latitude")

        plt.legend(loc="upper right", bbox_to_anchor=[1.1, 1.1], prop={"size": 10})

        plt.grid(True)

        show_or_save_fig(dir=dir, fig_name=fig_name, save_fig=save_fig, dpi=dpi)


if __name__ == "__main__":
    chosen_planets = ["Sun", "Venus", "Moon", "Mars"]
    date = {"year": 2020, "month": 5, "day": 5, "hour": 17, "minute": 14, "second": 0}
    map = Map(date=date, chosen_planets=chosen_planets)
    map.plot_map()
