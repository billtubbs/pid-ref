"""Basic unit tests for PID controller.

Tests the PID controller Python implementation in closed loop with
simulated systems.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np

from python_pid import PIDController
from tests.simulator import (
    create_first_order_system,
)


def test_pid_step_response_first_order():
    """Test PI controller on first-order system step response.

    Uses classic PI tuning rules for a first-order system:
    - Interactive form: Kc = 1/K, Ti = tau
    - Parallel form conversion: kp = Kc, ki = Kc/Ti
    - Discrete-time conversion: ki_discrete = ki_continuous * Ts

    This tuning provides a conservative, stable closed-loop response.
    """
    # System parameters
    K = 2.0  # Gain
    tau = 2.0  # Time constant

    # Create first-order plant simulator
    Ts = 0.1  # Sample time
    plant = create_first_order_system(K, tau, Ts)

    # Basic tuning for a continuous-time interactive PID
    # Interactive: u = Kc * (e + (1/Ti) * ∫e dt)
    Kc = 1.0 / K  # Controller gain = 1/K = 1.0
    Ti = tau  # Integral time constant

    # Convert to discrete-time parallel form
    kp = Kc  # kp = 1.0
    ki = Kc / Ti * Ts

    # PI controller (no derivative)
    kd = 0.0

    # Create PI controller
    controller = PIDController(kp=kp, ki=ki, kd=kd, TfTs=1.0)

    # Simulation parameters
    r = 1.0  # Step setpoint
    n_steps = 300  # Longer simulation for PI settling
    Tx = 1.0  # Normalized execution period (actual time = Ts)

    # Arrays to store results
    time = np.zeros(n_steps)
    outputs = np.zeros(n_steps)
    controls = np.zeros(n_steps)

    # Reset plant and controller
    plant.reset()
    controller.reset()

    # Run simulation
    y = 0.0
    for k in range(n_steps):
        # Compute control signal
        u = controller(r, y, Tx=Tx, auto=True)

        # Apply to plant
        y = plant.step(u)

        # Store results
        time[k] = k * Ts
        outputs[k] = y
        controls[k] = u

    # Check that system reaches steady state close to setpoint
    # PI controller should eliminate steady-state error
    steady_state_error = abs(outputs[-1] - r)
    assert steady_state_error < 0.01, (
        f"Steady-state error {steady_state_error:.4f} exceeds 1%"
    )

    # Check that output reaches 98% of setpoint (conservative PI)
    settling_idx = np.where(outputs > 0.98 * r)[0]
    assert len(settling_idx) > 0, "System did not reach 98% of setpoint"

    # Check stability - overshoot shouldn't exceed 25% for this tuning
    max_overshoot = (np.max(outputs) - r) / r
    assert max_overshoot < 0.25, f"Overshoot {max_overshoot:.2%} exceeds 25%"

    print("✓ PI controller test passed (Kc=1/K, Ti=tau tuning)")
    print(f"  Tuning: Kc={Kc:.2f}, Ti={Ti:.2f}s")
    print(f"  Gains: kp={kp:.2f}, ki={ki:.4f}, kd={kd:.2f}")
    print(f"  Final output: {outputs[-1]:.4f}")
    print(f"  Steady-state error: {steady_state_error:.4f}")
    print(f"  Settling time (98%): {time[settling_idx[0]]:.2f}s")
    print(f"  Max overshoot: {max_overshoot:.2%}")


def test_pid_proportional_only():
    """Test P-only controller (ki=0, kd=0)."""
    # System parameters
    K = 1.0
    tau = 1.0
    Ts = 0.1

    # Create system
    plant = create_first_order_system(K, tau, Ts)

    # P-only controller
    kp = 3.0
    controller = PIDController(kp=kp, ki=0.0, kd=0.0, TfTs=10.0)

    # Simulation
    r = 1.0
    n_steps = 100
    Tx = 1.0

    plant.reset()
    controller.reset()

    y = 0.0
    for k in range(n_steps):
        u = controller(r, y, Tx=Tx, auto=True)
        y = plant.step(u)

    # P-only controller should have steady-state error
    # Check that error exists (not within 1% of setpoint)
    ss_error = abs(y - r)
    assert ss_error > 0.01, "P-only controller should have steady-state error"

    print("✓ P-only controller test passed")
    print(f"  Steady-state error: {ss_error:.4f}")


def test_pid_manual_mode():
    """Test manual mode operation."""
    # Create controller
    controller = PIDController(kp=1.0, ki=0.5, kd=0.1, TfTs=10.0)

    # Test manual mode
    uman = 0.5
    y = 0.0
    u = controller(r=1.0, y=y, uman=uman, Tx=1.0, auto=False)

    # In manual mode, output should equal uman
    assert u == uman, f"Manual mode output {u} != {uman}"

    print("✓ Manual mode test passed")


def test_pid_saturation():
    """Test control signal saturation limits."""
    # Create controller with saturation limits
    controller = PIDController(
        kp=10.0, ki=5.0, kd=1.0, TfTs=10.0, umin=-1.0, umax=1.0
    )

    # Large error should saturate
    r = 10.0
    y = 0.0
    u = controller(r, y, Tx=1.0, auto=True)

    # Control signal should be saturated at umax
    assert u == 1.0, f"Control signal {u} not saturated at umax"

    # Reset and test negative saturation
    controller.reset()
    r = -10.0
    y = 0.0
    u = controller(r, y, Tx=1.0, auto=True)

    # Control signal should be saturated at umin
    assert u == -1.0, f"Control signal {u} not saturated at umin"

    print("✓ Saturation test passed")


if __name__ == "__main__":
    print("Running PID controller basic tests...\n")

    test_pid_step_response_first_order()
    test_pid_proportional_only()
    test_pid_manual_mode()
    test_pid_saturation()

    print("\n✓ All basic tests passed!")
