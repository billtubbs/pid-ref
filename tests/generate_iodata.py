"""Generate input-output data for PID controller tests.

This script reads test cases from test_cases.yaml, programmatically
generates error signals (step, random), runs the controllers, and saves
complete CSV files with error (e) and control (u) columns.
"""

import sys
from pathlib import Path

import numpy as np
import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from python_pid import PIDController


def load_test_config(yaml_file="tests/test_cases.yaml"):
    """Load test configuration from YAML file."""
    with open(yaml_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def generate_step_signal(length=10):
    """Generate step error signal.

    Step from 0.0 to 1.0 at third sample (after 2 intervals).

    Args:
        length: Number of samples (default: 10)

    Returns:
        list: Error signal values
    """
    signal = [0.0, 0.0] + [1.0] * (length - 2)
    return signal


def generate_random_signal(length=10, seed=42):
    """Generate random error signal.

    Random normal distribution with fixed seed for reproducibility.

    Args:
        length: Number of samples (default: 10)
        seed: Random seed (default: 42)

    Returns:
        list: Error signal values
    """
    np.random.seed(seed)
    signal = np.random.randn(length).tolist()
    return signal


def generate_signal(signal_type, length=10):
    """Generate error signal based on type.

    Args:
        signal_type: Type of signal ("step" or "random")
        length: Number of samples (default: 10)

    Returns:
        list: Error signal values
    """
    if signal_type == "step":
        return generate_step_signal(length)
    elif signal_type == "random":
        return generate_random_signal(length)
    else:
        raise ValueError(f"Unknown signal type: {signal_type}")


def generate_csv_datasets(config, base_dir="tests"):
    """Generate CSV files for each test case.

    Args:
        config: Test configuration from YAML
        base_dir: Base directory for tests (default: "tests")
    """
    base_path = Path(base_dir)
    data_path = base_path / "data"
    data_path.mkdir(exist_ok=True)

    controllers = config["controllers"]
    test_cases = config["test_cases"]

    # Generate CSV file for each test case
    for test_case in test_cases:
        controller_name = test_case["controller"]
        signal_type = test_case["signal"]
        csv_file = base_path / test_case["file"]

        # Get controller configuration
        ctrl_config = controllers[controller_name]

        # Generate error signal
        errors = generate_signal(signal_type)

        # Create controller
        controller = PIDController(
            kp=ctrl_config["kp"],
            ki=ctrl_config["ki"],
            kd=ctrl_config["kd"],
            umin=ctrl_config["umin"],
            umax=ctrl_config["umax"],
        )

        # Run controller on error signal
        outputs = []
        for e in errors:
            # Error = setpoint - measurement, so set r=e, y=0
            u = controller(r=e, y=0.0, Tx=1.0, auto=True)
            outputs.append(float(u))

        # Write CSV file
        with open(csv_file, "w", encoding="utf-8") as f:
            # Header
            f.write("e,u\n")
            # Data rows
            for e, u in zip(errors, outputs):
                f.write(f"{e},{u}\n")

        print(f"Generated: {csv_file}")
        print(f"  Controller: {controller_name}")
        print(f"  Signal: {signal_type}")
        print(f"  Samples: {len(errors)}\n")

    print(f"✓ Generated {len(test_cases)} CSV files in {data_path}")


if __name__ == "__main__":
    config = load_test_config()
    generate_csv_datasets(config)
