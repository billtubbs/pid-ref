# PID Controller Tests

This directory contains unit tests for the PID controller implementation.

## File Structure

```
tests/
├── test_cases.yaml        # Test case definitions
├── test_python_pid.py     # Parametrized pytest tests
├── generate_io_data.py    # Script to generate test data
├── step.csv               # Base signal: step sequence
├── random_1.csv           # Base signal: random sequence (seed=42)
├── random_2.csv           # Base signal: random sequence (seed=43)
├── true_to_false.csv      # Base signal: boolean switching
├── false_to_true.csv      # Base signal: boolean switching
└── data/                  # I/O data files for tests
    ├── P_step.csv
    ├── PI_step.csv
    ├── PID_step.csv
    └── ...
```

## Test Configuration (test_cases.yaml)

The YAML file is organized into two sections:

### 1. Controllers

Defines controller configurations:

```yaml
controllers:
  P:
    description: "P-only controller"
    kp: 1.0
    ki: 0.0
    kd: 0.0
    umin: -10.0
    umax: 10.0
```

### 2. Test Cases

Each test case specifies:
- **controller**: Controller configuration to use
- **io_data**: Path to I/O data CSV file
- **inputs_spec**: Specification for each input signal

```yaml
test_cases:
  P_step:
    controller: P
    io_data: data/P_step.csv
    inputs_spec:
      r: step.csv        # Can be constant or filename
      y: random_1.csv
      uff: 0.0
      uman: 0.0
      utrack: 0.0
      Tx: 1.0
      auto: true
      track: false
```

Input specifications can be either:
- **Constant values**: `0.0`, `1.0`, `true`, `false`
- **CSV filenames**: `step.csv`, `random_1.csv`, etc.

## CSV Data Formats

### Base Signal Files

Single column with header `value`:
```csv
value
0.0
0.0
1.0
1.0
...
```

### I/O Data Files

Complete input-output data with all controller inputs and output:
```csv
r,y,uff,uman,utrack,Tx,auto,track,u
0.0,0.497,0.0,0.0,0.0,1.0,true,false,0.003
0.0,-0.138,0.0,0.0,0.0,1.0,true,false,0.009
1.0,0.648,0.0,0.0,0.0,1.0,true,false,1.480
...
```

Columns:
- **r**: Reference (setpoint) signal
- **y**: Measurement signal
- **uff**: Feedforward control signal
- **uman**: Manual mode control signal
- **utrack**: Tracking signal for bumpless transfer
- **Tx**: Execution period (normalized)
- **auto**: Automatic mode flag (true/false)
- **track**: Tracking mode flag (true/false)
- **u**: Control signal output (expected value)

## Quick Start

### 1. Generate Test Data

Generate base signals and I/O data files for all test cases:

```bash
python3 tests/generate_io_data.py
```

This script:
1. Generates base signal sequences (step.csv, random_1.csv, etc.)
2. Reads test case definitions from test_cases.yaml
3. Loads or generates inputs based on inputs_spec
4. Runs the PID controller with specified inputs
5. Saves complete I/O data CSV files in tests/data/

### 2. Run Tests

```bash
# Run all tests
pytest tests/test_python_pid.py -v

# Run specific test
pytest tests/test_python_pid.py::test_pid_controller[P_step] -v
```

## How Tests Work

1. **test_python_pid.py** loads test cases from test_cases.yaml
2. For each test case:
   - Loads complete I/O data from the specified CSV file
   - Creates a controller with the specified configuration
   - Runs the controller with inputs from the CSV
   - Verifies outputs match expected values (within tolerance)

This approach ensures:
- **Repeatability**: Same inputs always produce same outputs
- **Cross-language validation**: I/O data can be used by other implementations
- **Comprehensive testing**: All controller inputs are tested

## Test Cases

Current test cases include:

| Test Case | Controller | Description |
|-----------|------------|-------------|
| P_step | P | P-only with step reference and random measurement |
| PI_step | PI | PI controller with step reference |
| PID_step | PID | Full PID with step reference |
| PID_antiwindup_step | PID_saturated | PID with saturation limits |
| PI_switch_manual | PI | Tests auto/manual mode switching |
| PI_switch_track | PI | Tests tracking mode for bumpless transfer |

## Adding New Test Cases

### 1. Add a new controller (if needed)

```yaml
# In controllers section of test_cases.yaml
PI_fast:
  description: "Faster PI controller"
  kp: 2.0
  ki: 1.0
  kd: 0.0
  umin: -10.0
  umax: 10.0
```

### 2. Add test case

```yaml
# In test_cases section
PI_fast_step:
  controller: PI_fast
  io_data: data/PI_fast_step.csv
  inputs_spec:
    r: step.csv
    y: random_1.csv
    uff: 0.0
    uman: 0.0
    utrack: 0.0
    Tx: 1.0
    auto: true
    track: false
```

### 3. Generate data and run tests

```bash
python3 tests/generate_io_data.py
pytest tests/test_python_pid.py -v
```

## Creating Custom Base Signals

To add new base signal sequences, modify `generate_io_data.py`:

```python
# In generate_base_signals() function
def generate_base_signals(base_dir="tests", length=10):
    # ... existing signals ...

    # Add your custom signal
    ramp_values = list(range(length))
    save_signal_csv(base_path / "ramp.csv", ramp_values)
```

Then reference it in test_cases.yaml:
```yaml
inputs_spec:
  r: ramp.csv
```

## Reusability

The modular structure enables:
- **Cross-language validation**: CSV files can be used by MATLAB, Julia, etc.
- **Implementation testing**: Verify any PID implementation with same data
- **Benchmarking**: Compare performance across implementations
- **Version control**: Track controller configs and expected outputs
