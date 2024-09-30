import pytest
import numpy as np
from PySpace2.planets.phase_angel import PhaseAngle  # Replace with the actual module name where the PhaseAngle class is located

# Mock the utilities if necessary
def mock_kernels_load(kernels):
    # Simulate kernel loading without actually loading anything
    pass

# Replace the original kernel loading function with the mock
PhaseAngle.kernels_load = staticmethod(mock_kernels_load)

class TestPhaseAngle:

    @pytest.fixture(scope="class")
    def phase_angle_instance(self):
        # Setup
        chosen_planets = ["Mars", "Jupiter", "Saturn", "Uran"]
        date = {"year": 2001, "month": 9, "day": 13, "hour": 5, "minute": 0, "second": 0}
        phase_angle_instance = PhaseAngle(delta_days=5000, date=date, chosen_planets=chosen_planets)
        yield phase_angle_instance
        # Teardown (if needed)

    def test_initialization(self, phase_angle_instance):
        # Ensure the instance was created successfully
        assert phase_angle_instance is not None
        assert phase_angle_instance._naif_chosen_planets is not None

    def test_add_planets_to_df(self, phase_angle_instance):
        # Check that the DataFrame has phase angle data for the chosen planets
        for planet in phase_angle_instance._naif_chosen_planets.keys():
            planet_angle_column = f"{planet}_phase_ang"
            planet_pos_column = f"{planet}_pos"
            assert planet_angle_column in phase_angle_instance._solar_system_data_frame.columns
            assert planet_pos_column in phase_angle_instance._solar_system_data_frame.columns

            # Ensure that the values are not empty
            assert phase_angle_instance._solar_system_data_frame[planet_angle_column].notnull().all()
            assert phase_angle_instance._solar_system_data_frame[planet_pos_column].notnull().all()

    def test_plot(self, phase_angle_instance):
        try:
            phase_angle_instance.plot(save_fig=False)  # Set save_fig=False to just test plotting functionality
        except Exception as e:
            pytest.fail(f"Plot method raised an exception: {e}")
