# PID Controller Reference Implementation

This repository contains implementations of the standard PID controller ([proportional-integral-derivative](https://en.wikipedia.org/wiki/Proportional–integral–derivative_controller)) based on the reference implementation by Sundström et al. (2024). The reference implementation uses the **incremental (velocity) form** of the PID controller, which provides intrinsic integrator anti-windup and bumpless transfer behavior.

**Source Repository**: https://github.com/copybit/pid

## Reference File Descriptions

The reference implementation is published in text files as pseudo-code.  Therefore it is not directly executable with any programming language compiler.  

The original text files forked from https://github.com/copybit/pid are included here for reference in the subdirectory [ref_txt](ref_txt).

### [ref_txt/pid.txt](ref_txt/pid.txt)
The main PID controller implementation. This file contains the core control algorithm that:
- Accepts reference signal (r), measurement (y), feedforward signal (uff), manual control signal (uman), and tracking signal (utrack)
- Implements the incremental form by computing control signal increments (Dup, Dui, Dud, Duff) rather than absolute values
- Handles automatic/manual mode switching and tracking mode for bumpless transfer
- Applies setpoint weighting (parameter b) to the proportional term
- Integrates the measurement filter Fy for derivative filtering
- Includes control signal saturation (umin, umax)
- Manages state initialization for P, PD, and PID modes

### [ref_txt/anti_windup.txt](ref_txt/anti_windup.txt)
Anti-windup logic for the integral term. This function prevents the integrator from accumulating error when the control signal is saturated by:
- Detecting when saturation occurs (upper, lower, or both limits)
- Preventing further integration in the direction of saturation
- Accepting the integral increment (Dui) and windup status as inputs
- Returning a modified integral increment that respects saturation constraints

### [ref_txt/Fy.txt](ref_txt/Fy.txt)
Measurement filter implementation. This file provides a second-order filter for:
- Filtering the process measurement (y) to obtain filtered output (yf)
- Computing the filtered derivative (dyf) for the D-term
- Automatically re-discretizing filter parameters when execution period (Tx) changes
- Using a state-space representation (a11, a12, a21, a22, b1, b2) for numerical stability

### [ref_txt/zoh_pid.txt](ref_txt/zoh_pid.txt)
Zero-order hold (ZOH) discretization for the measurement filter. This function:
- Computes the discrete-time filter parameters using exact ZOH discretization
- Accepts the filter time constant ratio (TfTs) and execution period (Tx)
- Returns the six state-space matrix coefficients (a11, a12, a21, a22, b1, b2)
- Ensures accurate filter behavior across different sample times

### [ref_txt/run.txt](ref_txt/run.txt)
Runtime execution loop. This file demonstrates how to integrate the PID controller into a control system by:
- Running the controller at a specified sample time (Ts)
- Reading signals from the runtime environment (setpoint, measurement, feedforward, etc.)
- Computing the actual execution period (Tx) to handle timing variations
- Calling the PID controller update function
- Implementing a sleep mechanism to maintain the desired sample rate

## Implementation Highlights

The reference implementation emphasizes several important aspects:

1. **Incremental Form**: Computes changes in control signal rather than absolute values, providing natural anti-windup
2. **Adaptive Timing**: Handles variations in execution period through the Tx parameter
3. **Measurement Filtering**: Uses a proper state-space filter for derivative computation
4. **Mode Switching**: Supports automatic/manual modes and tracking mode with bumpless transfer
5. **Proper Initialization**: Carefully manages state initialization for different controller types (P, PD, PID)

## Reference

E. Sundström, T. Hägglund, M. Bauer, J. Eker, K. Soltesz,
Reference Implementation of the PID Controller,
*IFAC-PapersOnLine*, Volume 58, Issue 7, 2024, Pages 370-375,
ISSN 2405-8963,
https://doi.org/10.1016/j.ifacol.2024.08.090

**GitHub Repository**: https://github.com/copybit/pid
