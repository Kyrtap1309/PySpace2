import pytest
from PySpace2.planets.earth import Earth  # Replace with the actual module name where the Earth class is located

# Mock the utilities if necessary
def mock_kernels_load(kernels):
    # You can implement a mock if you want to simulate the kernel loading behavior
    pass

# Replace the original kernel loading function with the mock
Earth.kernels_load = staticmethod(mock_kernels_load)

class TestEarth:

    @pytest.fixture(scope="class")
    def earth_instance(self):
        # Setup
        earth = Earth()
        yield earth
        # Teardown (if needed)

    def test_kernels_load(self, earth_instance):
        # Assuming kernels_load function is successful if no exception is raised
        assert earth_instance is not None  # Ensure the instance was created

    def test_earth_state_vector(self, earth_instance):
        assert earth_instance.earth_state_vector is not None
        assert len(earth_instance.earth_state_vector) == 6  # Check if the state vector has 6 elements

    def test_earth_sun_distance(self, earth_instance):
        assert earth_instance.earth_sun_distace > 0  # Distance should be positive
        assert earth_instance.au_earth_sun_distance > 0  # Distance in AU should also be positive

    def test_earth_sun_speed(self, earth_instance):
        assert earth_instance.earth_sun_speed > 0  # Speed should be positive
        assert earth_instance.earth_sun_speed_theory > 0  # Theoretical speed should also be positive

    def test_string_representation(self, earth_instance):
        info_str = str(earth_instance)
        assert "Earth location in relation to Sun" in info_str
        assert "Earth distance from Sun equals" in info_str
        assert "The Earth orbital speed around the Sun equals" in info_str
        assert "The theoretical Earth orbital speed around the Sun equals" in info_str
