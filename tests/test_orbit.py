import pytest
from unittest.mock import patch
from PySpace2.planets.orbit import Orbit
from datetime import datetime

# Mocking utilities if necessary
def mock_kernels_load(kernels):
    # Simulate kernel loading without actually loading anything
    pass

def mock_get_utc_time(date):
    # Return a fixed datetime object for testing
    return datetime(2000, 1, 1, 0, 0, 0)

class TestOrbit:

    @pytest.fixture(scope="class")
    def orbit_instance(self):
        # Setup
        date = {
            "year": 2000,
            "month": 1,
            "day": 1,
            "hour": 0,
            "minute": 0,
            "second": 0,
        }
        chosen_planet = "Earth"
        with patch('PySpace2.utilities.utilities.kernels_load', mock_kernels_load), \
             patch('PySpace2.utilities.utilities.get_utc_time', mock_get_utc_time):
            orbit_instance = Orbit(date, chosen_planet)
        yield orbit_instance
        # Teardown (if needed)

    def test_initialization(self, orbit_instance):
        # Ensure the instance was created successfully
        assert orbit_instance is not None
        assert hasattr(orbit_instance, 'orbit_semi_major_au')
        assert hasattr(orbit_instance, 'orbit_perihelion_au')
        assert hasattr(orbit_instance, 'orbit_ecentricity')
        assert hasattr(orbit_instance, 'orbit_inclination_deg')
        assert hasattr(orbit_instance, 'orbit_longitude_asc_node_deg')
        assert hasattr(orbit_instance, 'orbit_arg_perihelion_deg')
        assert hasattr(orbit_instance, 'orbit_period_years')

    def test_show_params(self, orbit_instance):
        # Check the output of show_params
        params = orbit_instance.show_params()
        assert isinstance(params, dict)
        assert 'semi_major_au' in params
        assert 'perihelion_au' in params
        assert 'ecentricity' in params
        assert 'inclination_deg' in params
        assert 'longitude_ascendation_node_deg' in params
        assert 'argument_perihelion_deg' in params
        assert 'orbital_period_years' in params