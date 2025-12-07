## C++ PID Controller Implementation

C++ implementation of the standard PID controller based on the reference by Sundström et al. (2024)[[1]](#reference). This implementation is compatible with Arduino C++ and most standard C++ compilers.

### Features

- **Incremental Form**: Computes changes in control signal for natural anti-windup
- **Measurement Filtering**: Second-order low-pass filter for derivative computation
- **Adaptive Timing**: Handles real-time variations in sampling period
- **Mode Switching**: Automatic/manual mode and tracking mode with bumpless transfer
- **Arduino Compatible**: Uses standard C++ features compatible with Arduino

### Files

- `pid.h` / `pid.cpp` - Main PID controller class
- `measurement_filter.h` / `measurement_filter.cpp` - Second-order measurement filter
- `anti_windup.h` / `anti_windup.cpp` - Anti-windup logic
- `zoh_pid.h` / `zoh_pid.cpp` - Zero-order hold discretization

### Usage Example

```cpp
#include "pid.h"

// Create PI controller (no derivative)
double kp = 0.5;      // Proportional gain
double ki = 0.1;      // Integral gain
double kd = 0.0;      // No derivative (PI controller)
double TfTs = 10.0;   // Filter time constant ratio

PIDController controller(kp, ki, kd, TfTs);

// In control loop
double r = 1.0;   // Setpoint
double y = 0.5;   // Measurement
double Tx = 1.0;  // Normalized execution period

double u = controller(r, y, 0.0, 0.0, 0.0, Tx, false, true);
```

### Compilation

**Standard C++:**
```bash
g++ -std=c++11 -o pid_test \\
    zoh_pid.cpp \\
    anti_windup.cpp \\
    measurement_filter.cpp \\
    pid.cpp \\
    your_test.cpp
```

**Arduino:**
Simply include all `.h` and `.cpp` files in your Arduino sketch folder.

### Dependencies

- Standard C++ library (`<cmath>`, `<algorithm>`, `<limits>`)
- Compatible with C++11 and later
- No external dependencies

### API Reference

#### PIDController Class

**Constructor:**
```cpp
PIDController(
    double kp,     // Proportional gain (required)
    double ki,     // Integral gain (required)
    double kd,     // Derivative gain (required)
    double TfTs = 10.0,        // Filter time constant ratio
    double umin = -infinity,   // Minimum control signal
    double umax = +infinity,   // Maximum control signal
    double u0 = 0.0,          // Bias term for P/PD control
    double b = 1.0            // Setpoint weight
);
```

**Compute Control Signal:**
```cpp
double operator()(
    double r,                          // Setpoint (required)
    double y,                          // Measurement (required)
    double uff = 0.0,                  // Feedforward signal
    double uman = 0.0,                 // Manual mode signal
    double utrack = 0.0,               // Tracking signal
    double Tx = 1.0,                   // Execution period
    bool track = false,                // Tracking mode flag
    bool auto_mode = true,             // Automatic mode flag
    WindupMode windup = WindupMode::NONE  // Windup status
);
```

**Reset Controller:**
```cpp
void reset();  // Reset all states to zero
```

#### WindupMode Enum

```cpp
enum class WindupMode {
    NONE,   // No saturation
    UPPER,  // Upper limit saturated
    LOWER,  // Lower limit saturated
    BOTH    // Both limits saturated
};
```

### Reference

[1] E. Sundström, T. Hägglund, M. Bauer, J. Eker, K. Soltesz,
"Reference Implementation of the PID Controller,"
*IFAC-PapersOnLine*, Volume 58, Issue 7, 2024, Pages 370-375,
ISSN 2405-8963,
[https://doi.org/10.1016/j.ifacol.2024.08.090](https://doi.org/10.1016/j.ifacol.2024.08.090)
