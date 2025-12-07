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


def load_test_config(tests_dir, filename="test_cases.yaml"):
    """Load test configuration from YAML file."""
    with open(Path(tests_dir) / filename, "r", encoding="utf-8") as f:
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
    signal = [initial_value] * switch_index + [not initial_value] * (
        length - switch_index
    )
    return signal


def generate_irregular_time_intervals(sigma=0.5, length=10):
    """Generate sample times with irregular intervals.

    Args:
        t_start: First sample time (default: 0.0)
        length: Number of samples (default: 10)

    Returns:
        list: Signal values
    """
    time_intervals = np.random.lognormal(mean=0.0, sigma=sigma, size=length)
    return time_intervals.tolist()


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
    """Load sequence of values from CSV file.

    Args:
        filepath: Path to CSV file

    Returns:
        list: Values
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


def generate_base_signals(data_dir, length=10):
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
    data_dir = Path(data_dir)
    data_dir.mkdir(exist_ok=True)

    # Generate step signal
    step_values = generate_step_signal(length)
    save_signal_csv(data_dir / "step.csv", step_values)
    print(f"Generated: {data_dir / 'step.csv'}")

    # Generate random signals
    random_1 = generate_random_signal(length=length, seed=42)
    save_signal_csv(data_dir / "random_1.csv", random_1)
    print(f"Generated: {data_dir / 'random_1.csv'}")

    random_2 = generate_random_signal(length=length, seed=43)
    save_signal_csv(data_dir / "random_2.csv", random_2)
    print(f"Generated: {data_dir / 'random_2.csv'}")

    # Generate boolean sequences
    true_to_false = generate_bool_sequence(True, 5, length=length)
    save_signal_csv(data_dir / "true_to_false.csv", true_to_false)
    print(f"Generated: {data_dir / 'true_to_false.csv'}")

    false_to_true = generate_bool_sequence(False, 5, length=length)
    save_signal_csv(data_dir / "false_to_true.csv", false_to_true)
    print(f"Generated: {data_dir / 'false_to_true.csv'}\n")

    # Generate irregular time samples
    irregular_time = generate_irregular_time_intervals(length=length)
    save_signal_csv(data_dir / "irregular_time.csv", irregular_time)
    print(f"Generated: {data_dir / 'irregular_time.csv'}")


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


def generate_io_data_files(config, data_dir, length=10):
    """Generate I/O data files for each test case.

    Args:
        config: Test configuration from YAML
        base_dir: Base directory for tests
        length: Number of samples
    """
    data_dir = Path(data_dir)

    controllers = config["controllers"]
    test_cases = config["test_cases"]

    # Generate I/O data for each test case
    for test_name, test_spec in test_cases.items():
        controller_name = test_spec["controller"]
        io_data_file = data_dir / test_spec["io_data"]
        inputs_spec = test_spec.get("inputs_spec", {})

        # Get controller configuration
        ctrl_config = controllers[controller_name]

        # Load or generate input signals
        t_values = inputs_spec.get("t")
        r_values = get_input_values(inputs_spec.get("r"), length, data_dir)
        y_values = get_input_values(
            inputs_spec.get("y", 0.0), length, data_dir
        )
        uff_values = get_input_values(
            inputs_spec.get("uff", 0.0), length, data_dir
        )
        uman_values = get_input_values(
            inputs_spec.get("uman", 0.0), length, data_dir
        )
        utrack_values = get_input_values(
            inputs_spec.get("utrack", 0.0), length, data_dir
        )
        Tx_values = get_input_values(
            inputs_spec.get("Tx", 1.0), length, data_dir
        )
        auto_values = get_input_values(
            inputs_spec.get("auto", True), length, data_dir
        )
        track_values = get_input_values(
            inputs_spec.get("track", False), length, data_dir
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

    print(f"✓ Generated {len(test_cases)} I/O data files in {data_dir}")


if __name__ == "__main__":
    # Configuration
    LENGTH = 10  # Number of samples in each sequence
    tests_dir = Path("tests")
    data_dir = tests_dir / "data"

    print("Step 1: Generating base signal sequences...\n")
    generate_base_signals(data_dir, length=LENGTH)

    print("Step 2: Loading test configuration...\n")
    config = load_test_config(tests_dir, filename="test_cases.yaml")

    print("Step 3: Generating I/O data files...\n")
    generate_io_data_files(config, data_dir, length=LENGTH)

    print("\n✓ All files generated successfully!")
