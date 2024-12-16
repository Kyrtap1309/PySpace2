import sqlite3

import numpy as np
import pandas as pd

from ..utilities.utilities import get_furnsh_path


class Comets:
    def __init__(self) -> None:
        """
        Initialize the Comets class with the database connection
        """
        _sql_path = get_furnsh_path("../database/comets.db")

        #Connect to the comets database
        _conn = sqlite3.connect(_sql_path)
        

        #Create dataframes with P and C type comets
        #Explanation of comets' types: https://en.wikipedia.org/wiki/List_of_comets_by_type
        self.p_type_def = pd.read_sql(
            'SELECT APHELION_AU, INCLINATION_DEG FROM comets_main WHERE ORBIT_TYPE="P"',
            _conn,
        )
        self.c_type_def = pd.read_sql(
            'SELECT APHELION_AU, INCLINATION_DEG FROM comets_main WHERE ORBIT_TYPE="C"',
            _conn,
        )

    def description(self, type: str) -> str:
        """
        Return the statistics of chosen type of comets

        Parameters:
        -----------
        type : str
            Type of comets 

        Return:
        -------
        description : str
            Statistcs of chosen type of comets
        """
        comet_dataframes = {"P": self.p_type_def, "C": self.c_type_def}
        chosen_dataframe = comet_dataframes[type]

        if type == "P":
            description = f"""
            Statistics of P type comets:
            {self.p_type_def.describe()} \n
            """
        elif type == "C":
            description = f"""
            Statistics of C type comets with an eccentricity (bound) < 1:
            {self.c_type_def.loc[self.c_type_def["ECCENTRICITY"]<1].describe()} \n

            Statistics of C type comets with an eccentricity (unbound) >= 1:
            {self.c_type_def.loc[self.c_type_def["ECCENTRICITY"]>=1].describe()} \n
            """

        return description