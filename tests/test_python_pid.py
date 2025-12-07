"""Parametrized unit tests for PID controller.

Tests the PID controller with comprehensive input signals and verifies
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
    for test_name, test_spec in config["test_cases"].items():
        test_case = {
            "name": test_name,
            "controller": config["controllers"][test_spec["controller"]],
            "io_data": test_spec["io_data"],
        }
        test_cases.append(test_case)

    return test_cases


def load_io_data(csv_file):
    """Load complete input-output data from CSV file.

    Expected CSV columns: r, y, uff, uman, utrack, Tx, auto, track, u

    Args:
        csv_file: Path to CSV file

    Returns:
        dict: Dictionary with keys for each column containing lists
    """
    import csv

    data = {
        "r": [],
        "y": [],
        "uff": [],
        "uman": [],
        "utrack": [],
        "Tx": [],
        "auto": [],
        "track": [],
        "u": [],
    }

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data["r"].append(float(row["r"]))
            data["y"].append(float(row["y"]))
            data["uff"].append(float(row["uff"]))
            data["uman"].append(float(row["uman"]))
            data["utrack"].append(float(row["utrack"]))
            data["Tx"].append(float(row["Tx"]))
            data["auto"].append(row["auto"].lower() == "true")
            data["track"].append(row["track"].lower() == "true")
            data["u"].append(float(row["u"]))

    return data


# Load test cases from YAML
TEST_CASES = load_test_cases()


@pytest.mark.parametrize("test_case", TEST_CASES, ids=lambda x: x["name"])
def test_pid_controller(test_case, tests_dir="tests", data_dir="data"):
    """Test PID controller with comprehensive input-output data.

    Loads complete I/O data from CSV (r, y, uff, uman, utrack, Tx,
    auto, track, u) and verifies controller produces expected outputs.
    """
    tests_dir = Path(tests_dir)

    # Create CSV file path
    csv_filepath = tests_dir / data_dir / test_case["io_data"]

    # Load complete I/O data
    data = load_io_data(csv_filepath)

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

    # Run controller with inputs from CSV
    outputs = []
    n_steps = len(data["r"])
    for i in range(n_steps):
        u = controller(
            r=data["r"][i],
            y=data["y"][i],
            uff=data["uff"][i],
            uman=data["uman"][i],
            utrack=data["utrack"][i],
            Tx=data["Tx"][i],
            track=data["track"][i],
            auto=data["auto"][i],
        )
        outputs.append(u)

    # Verify outputs match expected values (within tolerance)
    np.testing.assert_allclose(
        outputs,
        data["u"],
        rtol=1e-10,
        atol=1e-12,
        err_msg=f"Test case {test_case['name']} failed",
    )


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
