import pandas as pd
import numpy as np
import spiceypy

from .first_kepler import FirstKepler


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
