"""Discrete-time transfer function simulator for testing PID controllers.

This module provides a simulator for discrete-time systems represented
as transfer functions, used for testing and validating PID controller
implementations.
"""

import warnings

import numpy as np
from scipy import signal


class DiscreteTimeSimulator:
    """Discrete-time transfer function simulator.

    Simulates a discrete-time system specified as a transfer function
    G(z) = num(z) / den(z) with a given sample time.
    """

    def __init__(self, num, den, Ts):
        """Initialize the discrete-time simulator.

        Args:
            num: Numerator coefficients of the transfer function
                 (list or array)
            den: Denominator coefficients of the transfer function
                 (list or array)
            Ts: Sample time in seconds
        """
        self.num = np.atleast_1d(num)
        self.den = np.atleast_1d(den)
        self.Ts = Ts

        # Create discrete-time transfer function
        self.system = signal.dlti(self.num, self.den, dt=self.Ts)

        # Initialize state-space representation for simulation
        # Convert to state-space form for easier state tracking
        self.ss = self.system.to_ss()

        # Initialize state vector
        self.x = np.zeros(self.ss.A.shape[0])

        # Store current output
        self.y = 0.0

    def step(self, u):
        """Advance the simulation by one time step.

        Args:
            u: Input signal value

        Returns:
            float: Output signal value
        """
        # Compute output: y = C*x + D*u
        y_array = np.dot(self.ss.C, self.x) + np.dot(self.ss.D, u)
        self.y = float(np.asarray(y_array).item())

        # Update state: x[k+1] = A*x[k] + B*u[k]
        self.x = np.dot(self.ss.A, self.x) + np.dot(self.ss.B, u)

        return self.y

    def reset(self):
        """Reset the simulator state to zero."""
        self.x = np.zeros_like(self.x)
        self.y = 0.0

    def simulate(self, u_seq, x0=None):
        """Simulate the system for a sequence of inputs.

        Args:
            u_seq: Sequence of input values (array-like)
            x0: Initial state (optional, defaults to zero)

        Returns:
            tuple: (t, y) - time vector and output sequence
        """
        if x0 is not None:
            self.x = np.array(x0)

        u_seq = np.atleast_1d(u_seq)
        n = len(u_seq)

        # Time vector
        t = np.arange(n) * self.Ts

        # Output vector
        y = np.zeros(n)

        # Simulate
        for i, u in enumerate(u_seq):
            y[i] = self.step(u)

        return t, y


def create_first_order_system(K, tau, Ts):
    """Create a first-order discrete-time system.

    Creates a system with transfer function:
        G(s) = K / (tau*s + 1)

    which is then discretized using zero-order hold.

    Args:
        K: System gain
        tau: Time constant
        Ts: Sample time

    Returns:
        DiscreteTimeSimulator: Configured simulator
    """
    # Continuous-time transfer function
    num_c = [K]
    den_c = [tau, 1]

    # Convert to discrete-time using ZOH
    system_c = signal.TransferFunction(num_c, den_c)
    system_d = system_c.to_discrete(Ts, method="zoh")

    return DiscreteTimeSimulator(system_d.num, system_d.den, Ts)


def create_second_order_system(K, wn, zeta, Ts):
    """Create a second-order discrete-time system.

    Creates a system with transfer function:
        G(s) = K * wn^2 / (s^2 + 2*zeta*wn*s + wn^2)

    which is then discretized using zero-order hold.

    Args:
        K: System gain
        wn: Natural frequency (rad/s)
        zeta: Damping ratio
        Ts: Sample time

    Returns:
        DiscreteTimeSimulator: Configured simulator
    """
    # Continuous-time transfer function
    num_c = [K * wn**2]
    den_c = [1, 2 * zeta * wn, wn**2]

    # Convert to discrete-time using ZOH
    system_c = signal.TransferFunction(num_c, den_c)
    system_d = system_c.to_discrete(Ts, method="zoh")

    return DiscreteTimeSimulator(system_d.num, system_d.den, Ts)


def create_integrator(K, Ts):
    """Create a discrete-time integrator.

    Creates a system with transfer function:
        G(s) = K / s

    which is then discretized using zero-order hold.

    Args:
        K: Integrator gain
        Ts: Sample time

    Returns:
        DiscreteTimeSimulator: Configured simulator
    """
    # Continuous-time integrator
    num_c = [K]
    den_c = [1, 0]

    # Convert to discrete-time using ZOH
    system_c = signal.TransferFunction(num_c, den_c)
    system_d = system_c.to_discrete(Ts, method="zoh")

    return DiscreteTimeSimulator(system_d.num, system_d.den, Ts)
