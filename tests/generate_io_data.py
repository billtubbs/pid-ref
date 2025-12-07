"""Generate input-output data for PID controller tests.

This script:
1. Generates base signal sequences (step.csv, random_1.csv, etc.)
2. Reads test cases from test_cases.yaml
3. Loads or generates inputs based on inputs_spec
4. Runs the PID controller
5. Saves complete I/O data CSV files

CSV format: r, y, uff, uman, utrack, Tx, auto, track, u
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
    """Generate step signal.

    Step from 0.0 to 1.0 at third sample.

    Args:
        length: Number of samples (default: 10)

    Returns:
        list: Signal values
    """
    signal = [0.0, 0.0] + [1.0] * (length - 2)
    return signal


def generate_random_signal(length=10, seed=42):
    """Generate random signal.

    Random normal distribution with fixed seed.

    Args:
        length: Number of samples (default: 10)
        seed: Random seed (default: 42)

    Returns:
        list: Signal values
    """
    np.random.seed(seed)
    signal = np.random.randn(length).tolist()
    return signal


def generate_bool_sequence(initial_value, switch_index, length=10):
    """Generate boolean sequence that switches at given index.

    Args:
        initial_value: Initial boolean value
        switch_index: Index at which to switch value
        length: Total number of samples

    Returns:
        list: Boolean values
    """
    signal = [initial_value] * switch_index + [
        not initial_value
    ] * (length - switch_index)
    return signal


def save_signal_csv(filepath, values):
    """Save signal values to CSV file.

    Args:
        filepath: Path to CSV file
        values: List of values (float or bool)
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("value\n")
        for v in values:
            if isinstance(v, bool):
                f.write(f"{str(v).lower()}\n")
            else:
                f.write(f"{v}\n")


def load_signal_csv(filepath):
    """Load signal values from CSV file.

    Args:
        filepath: Path to CSV file

    Returns:
        list: Signal values
    """
    values = []
    with open(filepath, "r", encoding="utf-8") as f:
        next(f)  # Skip header
        for line in f:
            val = line.strip()
            # Try to parse as bool
            if val.lower() in ("true", "false"):
                values.append(val.lower() == "true")
            else:
                # Parse as float
                values.append(float(val))
    return values


def generate_base_signals(base_dir="tests", length=10):
    """Generate base signal sequences.

    Creates:
    - step.csv: Step signal (0->1 at index 2)
    - random_1.csv: Random signal (seed=42)
    - random_2.csv: Random signal (seed=43)
    - true_to_false.csv: Boolean (True->False at index 5)
    - false_to_true.csv: Boolean (False->True at index 5)

    Args:
        base_dir: Base directory for tests
        length: Number of samples in each signal
    """
    base_path = Path(base_dir)
    base_path.mkdir(exist_ok=True)

    # Generate step signal
    step_values = generate_step_signal(length)
    save_signal_csv(base_path / "step.csv", step_values)
    print(f"Generated: {base_path / 'step.csv'}")

    # Generate random signals
    np.random.seed(42)
    random_1 = np.random.randn(length).tolist()
    save_signal_csv(base_path / "random_1.csv", random_1)
    print(f"Generated: {base_path / 'random_1.csv'}")

    np.random.seed(43)
    random_2 = np.random.randn(length).tolist()
    save_signal_csv(base_path / "random_2.csv", random_2)
    print(f"Generated: {base_path / 'random_2.csv'}")

    # Generate boolean sequences
    true_to_false = generate_bool_sequence(True, 5, length)
    save_signal_csv(base_path / "true_to_false.csv", true_to_false)
    print(f"Generated: {base_path / 'true_to_false.csv'}")

    false_to_true = generate_bool_sequence(False, 5, length)
    save_signal_csv(base_path / "false_to_true.csv", false_to_true)
    print(f"Generated: {base_path / 'false_to_true.csv'}\n")


def get_input_values(spec, length, base_path):
    """Get input values from specification.

    Args:
        spec: Input specification (constant, filename, or None)
        length: Number of samples needed
        base_path: Base path for resolving filenames

    Returns:
        list: Input values
    """
    if spec is None:
        return None
    elif isinstance(spec, (int, float)):
        # Constant value
        return [spec] * length
    elif isinstance(spec, bool):
        # Constant boolean
        return [spec] * length
    elif isinstance(spec, str):
        # Filename - clean up double .csv if present
        filename = spec.replace(".csv.csv", ".csv")
        filepath = base_path / filename
        return load_signal_csv(filepath)
    else:
        raise ValueError(f"Invalid input specification: {spec}")


def generate_io_data_files(config, base_dir="tests", length=10):
    """Generate I/O data files for each test case.

    Args:
        config: Test configuration from YAML
        base_dir: Base directory for tests
        length: Number of samples
    """
    base_path = Path(base_dir)
    data_path = base_path / "data"
    data_path.mkdir(exist_ok=True)

    controllers = config["controllers"]
    test_cases = config["test_cases"]

    # Generate I/O data for each test case
    for test_name, test_spec in test_cases.items():
        controller_name = test_spec["controller"]
        io_data_file = base_path / test_spec["io_data"]
        inputs_spec = test_spec.get("inputs_spec", {})

        # Get controller configuration
        ctrl_config = controllers[controller_name]

        # Load or generate input signals
        r_values = get_input_values(
            inputs_spec.get("r"), length, base_path
        )
        y_values = get_input_values(
            inputs_spec.get("y", 0.0), length, base_path
        )
        uff_values = get_input_values(
            inputs_spec.get("uff", 0.0), length, base_path
        )
        uman_values = get_input_values(
            inputs_spec.get("uman", 0.0), length, base_path
        )
        utrack_values = get_input_values(
            inputs_spec.get("utrack", 0.0), length, base_path
        )
        Tx_values = get_input_values(
            inputs_spec.get("Tx", 1.0), length, base_path
        )
        auto_values = get_input_values(
            inputs_spec.get("auto", True), length, base_path
        )
        track_values = get_input_values(
            inputs_spec.get("track", False), length, base_path
        )

        # Create controller
        controller = PIDController(
            kp=ctrl_config["kp"],
            ki=ctrl_config["ki"],
            kd=ctrl_config["kd"],
            umin=ctrl_config["umin"],
            umax=ctrl_config["umax"],
        )

        # Run controller with specified inputs
        u_values = []
        for i in range(length):
            u = controller(
                r=r_values[i],
                y=y_values[i],
                uff=uff_values[i],
                uman=uman_values[i],
                utrack=utrack_values[i],
                Tx=Tx_values[i],
                track=track_values[i],
                auto=auto_values[i],
            )
            u_values.append(float(u))

        # Write I/O data CSV file
        with open(io_data_file, "w", encoding="utf-8") as f:
            # Header
            f.write("r,y,uff,uman,utrack,Tx,auto,track,u\n")
            # Data rows
            for i in range(length):
                f.write(
                    f"{r_values[i]},{y_values[i]},{uff_values[i]},"
                    f"{uman_values[i]},{utrack_values[i]},"
                    f"{Tx_values[i]},"
                    f"{str(auto_values[i]).lower()},"
                    f"{str(track_values[i]).lower()},"
                    f"{u_values[i]}\n"
                )

        print(f"Generated: {io_data_file}")
        print(f"  Test: {test_name}")
        print(f"  Controller: {controller_name}")
        print(f"  Samples: {length}\n")

    print(f"✓ Generated {len(test_cases)} I/O data files in {data_path}")


if __name__ == "__main__":
    # Configuration
    LENGTH = 10  # Number of samples in each sequence

    print("Step 1: Generating base signal sequences...\n")
    generate_base_signals(base_dir="tests", length=LENGTH)

    print("Step 2: Loading test configuration...\n")
    config = load_test_config()

    print("Step 3: Generating I/O data files...\n")
    generate_io_data_files(config, base_dir="tests", length=LENGTH)

    print("\n✓ All files generated successfully!")
