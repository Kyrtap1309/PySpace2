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
