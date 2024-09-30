import pytest
import pandas as pd
from PySpace2.planets.venus import Venus  # Replace with the actual module name

# Mocking utilities if necessary
def mock_kernels_load(kernels):
    # Simulate kernel loading without actually loading anything
    pass

# Replace the original kernel loading function with the mock
Venus.kernels_load = staticmethod(mock_kernels_load)

class TestVenus:

    @pytest.fixture(scope="class")
    def venus_instance(self):
        # Setup
        begin_date = {
            "year": 2001,
            "month": 9,
            "day": 13,
            "hour": 5,
            "minute": 0,
            "second": 0,
        }
        end_date = {
            "year": 2001,
            "month": 10,
            "day": 8,
            "hour": 3,
            "minute": 0,
            "second": 0,
        }
        venus_instance = Venus(begin_date, end_date)
        yield venus_instance
        # Teardown (if needed)

    def test_initialization(self, venus_instance):
        # Ensure the instance was created successfully
        assert venus_instance is not None
        assert isinstance(venus_instance._planets_dataframe, pd.DataFrame)
        assert not venus_instance._planets_dataframe.empty  # Ensure DataFrame is not empty

    def test_string_representation(self, venus_instance):
        # Check the output of __str__
        output = str(venus_instance)
        assert "Number of hours computed:" in output
        assert "Number of hours when we can take a photo:" in output

    def test_data_integrity(self, venus_instance):
        # Ensure that angles and photo-able column are computed correctly
        assert "Earth_Venus_Sun_Angle" in venus_instance._planets_dataframe.columns
        assert "Earth_Venus_Moon_Angle" in venus_instance._planets_dataframe.columns
        assert "Earth_Moon_Sun_Angle" in venus_instance._planets_dataframe.columns
        assert "photo-able" in venus_instance._planets_dataframe.columns

        # Check that the photo-able column is binary (0 or 1)
        assert all(venus_instance._planets_dataframe["photo-able"].isin([0, 1]))

        # Check specific conditions for being photo-able
        for _, row in venus_instance._planets_dataframe.iterrows():
            if row["photo-able"] == 1:
                assert row["Earth_Venus_Moon_Angle"] < 10.0
                assert row["Earth_Moon_Sun_Angle"] > 30.0
                assert row["Earth_Venus_Sun_Angle"] > 30.0

    def test_plot(self, venus_instance):
        try:
            venus_instance.plot(save_fig=False)  # Set save_fig=False to just test plotting functionality
        except Exception as e:
            pytest.fail(f"Plot method raised an exception: {e}")
