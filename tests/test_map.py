import pytest
import numpy as np
from PySpace2.planets.maps import Map  # Replace with the actual module name where the Map class is located

# Mock the utilities if necessary
def mock_kernels_load(kernels):
    # Simulate kernel loading without actually loading anything
    pass

# Replace the original kernel loading function with the mock
Map.kernels_load = staticmethod(mock_kernels_load)

class TestMap:

    @pytest.fixture(scope="class")
    def map_instance(self):
        # Setup
        chosen_planets = ["Sun", "Venus", "Moon", "Mars"]
        date = {"year": 2020, "month": 5, "day": 5, "hour": 17, "minute": 14, "second": 0}
        map_instance = Map(date=date, chosen_planets=chosen_planets)
        yield map_instance
        # Teardown (if needed)

    def test_kernels_load(self, map_instance):
        # Ensure the instance was created successfully
        assert map_instance is not None

    def test_initialization(self, map_instance):
        assert map_instance.chosen_planets == ["Sun", "Venus", "Moon", "Mars"]
        assert map_instance._utc_time_str is not None
        assert map_instance._et_time is not None

    def test_planet_positions(self, map_instance):
        for planet in map_instance.chosen_planets:
            longitudes = map_instance._map_dataframe[f"{planet}_longtitude"].to_numpy()
            latitudes = map_instance._map_dataframe[f"{planet}_latitude"].to_numpy()
            assert len(longitudes) > 0  # Ensure there are computed longitudes
            assert len(latitudes) > 0    # Ensure there are computed latitudes

    def test_ecliptic_coordinates(self, map_instance):
        assert "Ecliptic_longtitudes" in map_instance._ecliptic_dataframe.columns
        assert "Ecliptic_latitudes" in map_instance._ecliptic_dataframe.columns
        assert len(map_instance._ecliptic_dataframe) > 0  # Ensure ecliptic data is populated

    def test_equatorial_coordinates(self, map_instance):
        assert "Equator_long" in map_instance._ecliptic_dataframe.columns
        assert "Equator_lat" in map_instance._ecliptic_dataframe.columns
        assert len(map_instance._ecliptic_dataframe) > 0  # Ensure equatorial data is populated

    def test_plot_map(self, map_instance):
        try:
            map_instance.plot_map(save_fig=False)  # Set save_fig=False to just test plotting functionality
        except Exception as e:
            pytest.fail(f"Plot map method raised an exception: {e}")
