import pytest
import numpy as np
from PySpace2.planets.first_kepler import FirstKepler  # Replace with the actual module name where the FirstKepler class is located

# Mock the utilities if necessary
def mock_kernels_load(kernels):
    # Simulate kernel loading without actually loading anything
    pass

# Replace the original kernel loading function with the mock
FirstKepler.kernels_load = staticmethod(mock_kernels_load)

class TestFirstKepler:

    @pytest.fixture(scope="class")
    def kepler_instance(self):
        # Setup
        date = {"year": 2001, "month": 9, "day": 13, "hour": 5, "minute": 0, "second": 0}
        kepler = FirstKepler(delta_days=5000, date=date)
        yield kepler
        # Teardown (if needed)

    def test_kernels_load(self, kepler_instance):
        # Ensure the instance was created successfully
        assert kepler_instance is not None

    def test_initialization(self, kepler_instance):
        assert kepler_instance.init_time is not None
        assert kepler_instance.end_time is not None
        assert kepler_instance.time_array.shape[0] == 5000  # Should match delta_days

    def test_solar_system_barycentre_pos_array(self, kepler_instance):
        assert kepler_instance._solar_system_barycentre_pos_array is not None
        assert kepler_instance._solar_system_barycentre_pos_array.shape == (5000, 3)  # 5000 positions in 3D space

    def test_sun_radius(self, kepler_instance):
        assert kepler_instance._sun_radius > 0  # Sun radius should be a positive value

    def test_string_representation(self, kepler_instance):
        info_str = str(kepler_instance)
        assert "Start day:" in info_str
        assert "End day:" in info_str
        assert "Position of the Solar System Barycentre" in info_str
        assert "Distance between the Solar System Barycentre" in info_str

    def test_trajectory_method(self, kepler_instance):
        try:
            kepler_instance.trajectory(save_fig=False)  # We can set save_fig=False to just test plotting functionality
        except Exception as e:
            pytest.fail(f"Trajectory method raised an exception: {e}")
