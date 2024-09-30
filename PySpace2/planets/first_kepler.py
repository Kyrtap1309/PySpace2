import datetime
import os
import numpy as np
import spiceypy
from matplotlib import pyplot as plt


from ..utilities.utilities import (
    kernels_load,
    create_folder_if_not_exists,
    show_or_save_fig,
    get_utc_time,
)
from ..utilities.constants import NAIF_PLANETS_ID


class FirstKepler:

    def __init__(self, delta_days: int, date: dict) -> None:
        """
        Initialize the class with a time range and date for the trajectory computation.

        Parameters:
        -----------
        delta_days : int
            Number of days to compute the trajectory for.
        date : dict
            Starting date for the computation (year, month, day, hour, minute, second).
        """

        # spicepy needs a kernels loaded to work properly
        kernels = ["../kernels/spk/de432s.bsp", "../kernels/pck/pck00010.tpc"]
        kernels_load(kernels)

        self.init_time = get_utc_time(date)
        self.end_time = self.init_time + datetime.timedelta(days=delta_days)

        # Initialization of UTC time
        self.init_time_utc_str = self.init_time.strftime("%Y-%m-%dT%H:%M:%S")
        self.end_time_utc_str = self.end_time.strftime("%Y-%m-%dT%H:%M:%S")

        # Ephemeris time
        init_et_time = spiceypy.utc2et(self.init_time_utc_str)
        end_et_time = spiceypy.utc2et(self.end_time_utc_str)

        # Create numpy array with one day interval between start and end day
        self.time_array = np.linspace(init_et_time, end_et_time, delta_days)

        # Array with all positions of solar system barycentre
        self._solar_system_barycentre_pos = []

        for time in self.time_array:
            _position, _ = spiceypy.spkgps(
                targ=NAIF_PLANETS_ID["SSB"],
                et=time,
                ref="ECLIPJ2000",
                obs=NAIF_PLANETS_ID["Sun"],
            )
            self._solar_system_barycentre_pos.append(_position)

        # convert to numpy array
        self._solar_system_barycentre_pos_array = np.array(
            self._solar_system_barycentre_pos
        )

        # import sun radius
        _, sun_radius_arr = spiceypy.bodvcd(
            bodyid=NAIF_PLANETS_ID["Sun"], item="RADII", maxn=3
        )
        self._sun_radius = sun_radius_arr[0]

        # Scalled solar system barycentre position (in Sun radii)
        self._solar_system_barycentre_pos_scalled = (
            self._solar_system_barycentre_pos_array / self._sun_radius
        )

    @property
    def solar_system_barycentre_pos_array(self):
        """Get the positions of the solar system barycenter as a numpy array."""
        return self._solar_system_barycentre_pos_array

    @property
    def solar_system_barycentre_pos_scalled(self):
        """Get the scaled positions of the solar system barycenter in Sun radii."""
        return self._solar_system_barycentre_pos_scalled

    @property
    def sun_radius(self):
        """Get the radius of the Sun."""
        return self._sun_radius

    def __str__(self) -> str:

        # Print the starting and end times
        info = f"""\tStart day: {self.init_time_utc_str}
        End day: {self.end_time_utc_str}
        """
        info += """Position of the Solar System Barycentre with relation to the\n
        centre of the Sun (at inital time): \n
        X = %s km\n
        Y = %s km\n
        Z = %s km\n\n """ % tuple(
            np.round(self._solar_system_barycentre_pos_array[0])
        )

        info += f"""\tDistance between the Solar System Barycentre w.r.t the\n
        centre of the Sun (at initial time): \n
        d = {round(np.linalg.norm(self._solar_system_barycentre_pos_array[0]))} km\n"""
        return info

    def trajectory(
        self,
        save_fig: bool = True,
        dpi: str = 500,
        fig_name: str = "barycentre_trajectory.png",
        dir: str = "./plots",
    ) -> None:
        """
        Plot the trajectory of solar system barycentre with relation to the Sun

        Parameters:
        -----------
        save_fig: bool
            If plot is supposed to be saved instead of showed
        dpi: int
            dpi of saved plot
        fig_name: str
            name of plot
        dir: str
            relative (to pwd) path of dir with plots
        """

        # Plotting trajectory of solar system barycentre (only needed x and y coordinates)
        solar_system_barycentre_pos_scalled_plane = (
            self._solar_system_barycentre_pos_scalled[:, 0:2]
        )

        plt.style.use("dark_background")

        fig, ax = plt.subplots(figsize=(12, 8))

        # Create a yellow circle that represents the Sun, add it to the ax
        sun = plt.Circle((0.0, 0.0), 1.0, color="yellow", alpha=0.8)
        ax.add_artist(sun)

        ax.plot(
            solar_system_barycentre_pos_scalled_plane[:, 0],
            solar_system_barycentre_pos_scalled_plane[:, 1],
            ls="solid",
            color="royalblue",
        )

        ax.set_aspect("equal")
        ax.grid(True, linestyle="dashed", alpha=0.5)
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)

        ax.set_xlabel("X in Sun-Radius")
        ax.set_ylabel("Y in Sun-Radius")

        show_or_save_fig(dir=dir, fig_name=fig_name, save_fig=save_fig, dpi=dpi)


if __name__ == "__main__":
    date = {"year": 2001, "month": 9, "day": 13, "hour": 5, "minute": 0, "second": 0}
    first_kepler = FirstKepler(date=date, delta_days=5000)
    print(first_kepler)
    first_kepler.trajectory()
