import pytest
import pandas as pd
import numpy as np
from PySpace2.planets.solar_system import SolarSystem  # Replace with the actual module name

# Mocking utilities if necessary
def mock_show_or_save_fig(*args, **kwargs):
    # Simulate show or save functionality without actually performing any I/O
    pass

# Replace the original show_or_save_fig function with the mock
SolarSystem.show_or_save_fig = staticmethod(mock_show_or_save_fig)

class TestSolarSystem:

    @pytest.fixture(scope="class")
    def solar_system_instance(self):
        # Setup
        date = {"year": 2001, "month": 9, "day": 13, "hour": 5, "minute": 0, "second": 0}
        solar_system_instance = SolarSystem(delta_days=5000, date=date)
        yield solar_system_instance
        # Teardown (if needed)

    def test_initialization(self, solar_system_instance):
        # Ensure the instance was created successfully
        assert solar_system_instance is not None
        assert isinstance(solar_system_instance._solar_system_data_frame, pd.DataFrame)
        assert not solar_system_instance._solar_system_data_frame.empty  # Ensure DataFrame is not empty

    def test_data_frame_columns(self, solar_system_instance):
        # Check that the expected columns are present in the DataFrame
        expected_columns = ["ET", "UTC", "barycentre_pos", "barycentre_pos_scalled", "Barycentre_distance"]
        for column in expected_columns:
            assert column in solar_system_instance._solar_system_data_frame.columns

    def test_barycentre_distance_computation(self, solar_system_instance):
        # Check that barycentre distance values are computed and valid
        assert "Barycentre_distance" in solar_system_instance._solar_system_data_frame.columns
        
        # Ensure Barycentre_distance is a numeric column and does not contain NaN
        assert pd.api.types.is_numeric_dtype(solar_system_instance._solar_system_data_frame["Barycentre_distance"])
        assert not solar_system_instance._solar_system_data_frame["Barycentre_distance"].isnull().any()

        # Check that the values are within an expected range (this depends on your specific implementation)
        assert all(solar_system_instance._solar_system_data_frame["Barycentre_distance"] >= 0)

    def test_plot(self, solar_system_instance):
        try:
            solar_system_instance.plot(save_fig=False)  # Set save_fig=False to test plotting functionality
        except Exception as e:
            pytest.fail(f"Plot method raised an exception: {e}")

