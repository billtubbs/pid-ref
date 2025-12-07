# PID Controller Reference Implementation

Simple, real-time executable Python implementation of the standard PID ([proportional-integral-derivative](https://en.wikipedia.org/wiki/Proportional–integral–derivative_controller)) controller defined by Sundström, Hägglund, Bauer, Eker, and Soltesz in 2024[[1]](#reference).  Since they defined the reference implementation using pseudo-code, it is not directly executable with any language compiler.

The purpose of this repository is to demonstrate a working implementation that could serve as a comparable test for other implementations.

## Features

The reference PID implementation by Sundström et al. includes the following features:

1. **Incremental Form**: Computes changes in control signal rather than absolute values, providing natural anti-windup prevention
2. **Measurement Filtering**: Incorporates a second-order low pass filter to reduce measurement noise
3. **Adaptive Timing**: Handles real-time variations in sampling period
4. **Mode Switching**: Supports automatic/manual mode switching and tracking mode with bumpless transfer
5. **Proper Initialization**: Manages state initialization for different controller types (P, PD, PID)


## Reference Implementation Files

The reference implementation pseudo-code was published by Sundström et al. in their paper [[1]](#reference) and also in the following GitHub repository.

**Source**: https://github.com/copybit/pid

I include forked copies of this pseudo-code here for reference in the subdirectory [ref_txt](ref_txt).

### [pid.txt](ref_txt/pid.txt)
The main PID controller implementation. This file contains the core control algorithm that:
- Accepts reference signal (r), measurement (y), feedforward signal (uff), manual control signal (uman), and tracking signal (utrack)
- Implements the incremental form by computing control signal increments (Dup, Dui, Dud, Duff) rather than absolute values
- Handles automatic/manual mode switching and tracking mode for bumpless transfer
- Applies setpoint weighting (parameter b) to the proportional term
- Integrates the measurement filter Fy for derivative filtering
- Includes control signal saturation (umin, umax)
- Manages state initialization for P, PD, and PID modes

### [anti_windup.txt](ref_txt/anti_windup.txt)
Anti-windup logic for the integral term. This function prevents the integrator from accumulating error when the control signal is saturated by:
- Detecting when saturation occurs (upper, lower, or both limits)
- Preventing further integration in the direction of saturation
- Accepting the integral increment (Dui) and windup status as inputs
- Returning a modified integral increment that respects saturation constraints

### [Fy.txt](ref_txt/Fy.txt)
Measurement filter implementation. This file provides a second-order filter for:
- Filtering the process measurement (y) to obtain filtered output (yf)
- Computing the filtered derivative (dyf) for the D-term
- Automatically re-discretizing filter parameters when execution period (Tx) changes
- Using a state-space representation (a11, a12, a21, a22, b1, b2) for numerical stability

### [zoh_pid.txt](ref_txt/zoh_pid.txt)
Zero-order hold (ZOH) discretization for the measurement filter. This function:
- Computes the discrete-time filter parameters using exact ZOH discretization
- Accepts the filter time constant ratio (TfTs) and execution period (Tx)
- Returns the six state-space matrix coefficients (a11, a12, a21, a22, b1, b2)
- Ensures accurate filter behavior across different sample times

### [run.txt](ref_txt/run.txt)
Runtime execution loop. This file demonstrates how to integrate the PID controller into a control system by:
- Running the controller at a specified sample time (Ts)
- Reading signals from the runtime environment (setpoint, measurement, feedforward, etc.)
- Computing the actual execution period (Tx) to handle timing variations
- Calling the PID controller update function
- Implementing a sleep mechanism to maintain the desired sample rate

## Python Implementation Usage Example

This example demonstrates how to initialize a PI controller and set up
a runtime environment.

### Basic PI Controller

```python
from python_pid import PIDController, PIDRuntime

# Initialize PI controller
kp = 0.5      # Proportional gain
ki = 0.1      # Integral gain (discrete-time)
kd = 0.0      # No derivative (PI controller)
TfTs = 10.0   # Filter time constant expressed as number of sample periods

controller = PIDController(kp=kp, ki=ki, kd=kd, TfTs=TfTs)
```

### Runtime Environment

```python
# Set up runtime
Ts = 0.1  # Sample time: 100 ms
runtime = PIDRuntime(controller, Ts=Ts)

# Override these methods to connect to your system
class MyRuntime(PIDRuntime):
    def get_r(self):
        # Read setpoint from your system
        return read_setpoint()

    def get_y(self):
        # Read measurement from your system
        return read_sensor()

    def set_u(self, u):
        # Send control signal to actuator
        write_actuator(u)

# Run the control loop
my_runtime = MyRuntime(controller, Ts=0.1)
my_runtime.run()  # Runs until my_runtime.stop = True
```

### Simple Single-Step Usage

```python
# For direct implementation without the runtime helper
r = 1.0   # Setpoint
y = 0.5   # Measurement
Tx = 1.0  # Normalized execution period

u = controller(r, y, Tx=Tx, auto=True)
```

## Nomenclature

See [[1]](#reference) for details.

| Variable | Function | Explanation | Paper Section |
|----------|----------|-------------|---------------|
| `a11`, `a12`, `a21`, `a22` | `zoh_Fy`, `Fy` | Discrete-time measurement filter system matrix elements | 3.4 |
| `auto` | `PID` | Boolean flag set to true in auto mode; false in manual mode | 3.6 |
| `b` | `PID` | Setpoint weight | 3.3 |
| `b1`, `b2` | `zoh_Fy`, `Fy` | Discrete-time measurement filter input matrix elements | 3.4 |
| `Du` | `PID` | Control signal increment | 3.1 |
| `Duff` | `PID` | Feed-forward control signal increment | 3.1 |
| `Dup`, `Dui`, `Dud` | `PID` | Control signal term increments (P, I, D) | 3.1 |
| `dyf` | `Fy`, `PID` | Filtered measurement derivative | 3.4 |
| `h1`, `h2`, `h3`, `h4` | `zoh_Fy` | Help variables to encode measurement filter discretization | 3.4 |
| `kp`, `ki`, `kd` | `PID` | Linear form controller gains (proportional, integral, derivative) | 3.1 |
| `r` | `PID` | Setpoint (reference) | 3.3 |
| `stop` | `run` | Boolean flag to stop execution | - |
| `t0`, `t`, `t_old` | `run` | Wall time stamps: at beginning of run function; before PID update; before previous PID update | 3.5 |
| `TfTs` | `Fy`, `zoh_Fy` | Number of filter time constants per nominal sampling period: Tf/Ts | 3.5 |
| `track` | `PID` | Boolean flag indicating tracking mode | - |
| `Ts` | `run` | Nominal PID sampling time | 3.5 |
| `Tx` | `PID`, `Fy`, `zoh_Fy` | Scale factor that relates nominal update period to actual: Tx*Ts | 3.5 |
| `Tx_old` | `Fy` | Previous value of Tx | 3.5 |
| `u` | `PID` | Control signal | 3.1 |
| `u0` | `PID` | Bias term in P and PD control | 3.3 |
| `uff` | `PID` | Feedforward control signal | 3.1 |
| `uff_old` | `PID` | Previous feed-forward control signal | 3.1 |
| `uman` | `PID` | Manual control signal | 3.6 |
| `umin`, `umax` | `PID` | Control signal saturation limits | 3.7 |
| `up_old`, `ud_old` | `PID` | P- and D-values from last iteration | 3.1 |
| `utrack` | `PID` | Tracking signal | - |
| `u_old` | `PID` | Previous control signal (state in the controller) | 3.1 |
| `windup` | `anti_windup`, `PID` | Externally generated windup flag | 3.7 |
| `y` | `PID`, `Fy` | Measurement signal | 3.4 |
| `yf` | `Fy`, `PID` | Filtered measurement signal | 3.4 |
| `yf1` | `Fy` | Help variable in the filter update function | 3.4 |

## Reference

[1] E. Sundström, T. Hägglund, M. Bauer, J. Eker, K. Soltesz,
"Reference Implementation of the PID Controller,"
*IFAC-PapersOnLine*, Volume 58, Issue 7, 2024, Pages 370-375,
ISSN 2405-8963,
[https://doi.org/10.1016/j.ifacol.2024.08.090](https://doi.org/10.1016/j.ifacol.2024.08.090)

**GitHub Repository**: https://github.com/copybit/pid
