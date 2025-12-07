"""Parametrized unit tests for PID controller.

Tests the PID controller with predefined error signals and verifies
outputs match expected values from CSV files.

Test cases are loaded from test_cases.yaml and I/O data from CSV files.
"""

import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from python_pid import PIDController


def load_test_cases():
    """Load test cases from YAML file."""
    yaml_file = Path(__file__).parent / "test_cases.yaml"
    with open(yaml_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Build test cases list
    test_cases = []
    for tc in config["test_cases"]:
        test_case = {
            "name": tc["name"],
            "controller": config["controllers"][tc["controller"]],
            "file": tc["file"],
        }
        test_cases.append(test_case)

    return test_cases


def load_csv_data(csv_file):
    """Load error and control signals from CSV file.

    Args:
        csv_file: Path to CSV file with columns e,u

    Returns:
        tuple: (errors, controls) as lists
    """
    errors = []
    controls = []

    with open(csv_file, "r", encoding="utf-8") as f:
        # Skip header
        next(f)
        # Read data
        for line in f:
            e, u = line.strip().split(",")
            errors.append(float(e))
            controls.append(float(u))

    return errors, controls


# Load test cases from YAML
TEST_CASES = load_test_cases()


@pytest.mark.parametrize("test_case", TEST_CASES, ids=lambda x: x["name"])
def test_pid_controller(test_case):
    """Test PID controller with CSV input-output data.

    Verifies that the controller produces expected outputs for
    different configurations (P, PI, PID, PID+anti-windup) and
    error signals (step, random).
    """
    # Get CSV file path
    csv_file = Path(__file__).parent / test_case["file"]

    # Skip if CSV file doesn't exist yet
    if not csv_file.exists():
        pytest.skip(f"CSV file not found: {csv_file}")

    # Load expected I/O data
    errors, expected_outputs = load_csv_data(csv_file)

    # Get controller configuration
    ctrl = test_case["controller"]

    # Create controller with test parameters
    controller = PIDController(
        kp=ctrl["kp"],
        ki=ctrl["ki"],
        kd=ctrl["kd"],
        umin=ctrl["umin"],
        umax=ctrl["umax"],
    )

    # Run controller on error signal
    outputs = []
    for e in errors:
        # Error = setpoint - measurement, so set r=e, y=0
        u = controller(r=e, y=0.0, Tx=1.0, auto=True)
        outputs.append(u)

    # Verify outputs match expected values (within tolerance)
    np.testing.assert_allclose(
        outputs,
        expected_outputs,
        rtol=1e-10,
        atol=1e-12,
        err_msg=f"Test case {test_case['name']} failed",
    )


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
