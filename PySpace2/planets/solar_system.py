import pandas as pd
import numpy as np
import spiceypy

from matplotlib import pyplot as plt

from .first_kepler import FirstKepler
from ..utilities.utilities import show_or_save_fig


class SolarSystem(FirstKepler):
    def __init__(self, delta_days: int, date: dict) -> None:
        """
        Expand FirstKepler init with solar system dataframe

        Parameters:
        -----------
        delta_days : int
            Number of days to compute the trajectory for.
        date : dict
            Starting date for the computation (year, month, day, hour, minute, second).
        """
        super().__init__(delta_days, date)

        self._create_solar_system_df()

    def _create_solar_system_df(self) -> None:
        """
        Create solar system dataframe.
        """
        self._solar_system_data_frame = pd.DataFrame()

        # Creating a column with ETs in dataframe
        self._solar_system_data_frame.loc[:, "ET"] = self.time_array

        # Creating a column with UTCs in dataframe
        self._solar_system_data_frame.loc[:, "UTC"] = self._solar_system_data_frame[
            "ET"
        ].apply(lambda et: spiceypy.et2datetime(et=et).date())

        # Creating a column with a position of barycentre
        # of the solar system
        self._solar_system_data_frame.loc[:, "barycentre_pos"] = (
            self._solar_system_barycentre_pos
        )

        self._solar_system_data_frame.loc[:, "barycentre_pos_scalled"] = (
            self._solar_system_data_frame["barycentre_pos"].apply(
                lambda x: x / self._sun_radius
            )
        )

        # Creating a column with a distance between barycentre
        # and sun
        self._solar_system_data_frame.loc[:, "Barycentre_distance"] = (
            self._solar_system_data_frame["barycentre_pos_scalled"].apply(
                lambda x: np.linalg.norm(x)
            )
        )

    def plot(
        self,
        save_fig: bool = True,
        dpi: str = 500,
        fig_name: str = "solar_system_barycentrum_distance_plot.png",
        dir: str = "./plots",
    ) -> None:
        """
        Plot solar system barycentre distance from sun with time

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

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(
            self._solar_system_data_frame["UTC"],
            self._solar_system_data_frame["Barycentre_distance"],
            color="tab:blue",
        )

        ax.set_xlabel("UTC Date")
        ax.set_ylabel(
            "Solar System Barycentre Distance from Sun [Sun Radii]", color="tab:blue"
        )
        ax.tick_params(axis="y", labelcolor="tab:blue")

        ax.set_xlim(
            min(self._solar_system_data_frame["UTC"]),
            max(
                self._solar_system_data_frame["UTC"],
            ),
        )
        ax.set_ylim(0, 2)

        ax.grid(axis="x", linestyle="dashed", alpha=0.5)

        show_or_save_fig(dir=dir, fig_name=fig_name, save_fig=save_fig, dpi=dpi)


if __name__ == "__main__":
    date = {"year": 2001, "month": 9, "day": 13, "hour": 5, "minute": 0, "second": 0}
    solar_system = SolarSystem(delta_days=5000, date=date)
    solar_system.plot()
