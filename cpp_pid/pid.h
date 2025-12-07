/**
 * @file pid.h
 * @brief PID controller implementation
 *
 * This file provides a PID controller class using the incremental
 * (velocity) form, which provides intrinsic integrator anti-windup and
 * bumpless transfer behavior.
 */

#ifndef PID_H
#define PID_H

#include "anti_windup.h"
#include "measurement_filter.h"
#include <limits>

/**
 * @brief PID controller using incremental (velocity) form
 *
 * Implements the reference PID controller algorithm from Sundström et
 * al. (2024) with incremental form, measurement filtering, and
 * automatic/manual mode switching.
 */
class PIDController {
public:
    /**
     * @brief Constructor
     *
     * @param kp Proportional gain
     * @param ki Integral gain
     * @param kd Derivative gain
     * @param TfTs Filter time constant as multiple of nominal sample
     *             time (default: 10.0)
     * @param umin Minimum control signal (default: -infinity)
     * @param umax Maximum control signal (default: +infinity)
     * @param u0 Bias term for P or PD control (default: 0.0)
     * @param b Setpoint weight for proportional term (default: 1.0)
     */
    PIDController(
        double kp,
        double ki,
        double kd,
        double TfTs = 10.0,
        double umin = -std::numeric_limits<double>::infinity(),
        double umax = std::numeric_limits<double>::infinity(),
        double u0 = 0.0,
        double b = 1.0);

    /**
     * @brief Compute the PID control signal
     *
     * @param r Reference (setpoint) signal
     * @param y Process measurement
     * @param uff Feedforward control signal (default: 0.0)
     * @param uman Manual mode control signal (default: 0.0)
     * @param utrack Tracking signal for bumpless transfer (default: 0.0)
     * @param Tx Execution period normalized (default: 1.0)
     * @param track Tracking mode flag (default: false)
     * @param auto_mode Automatic mode flag (default: true)
     * @param windup Windup status (default: NONE)
     * @return Control signal u
     */
    double operator()(
        double r,
        double y,
        double uff = 0.0,
        double uman = 0.0,
        double utrack = 0.0,
        double Tx = 1.0,
        bool track = false,
        bool auto_mode = true,
        WindupMode windup = WindupMode::NONE);

    /**
     * @brief Reset the controller state to zero
     */
    void reset();

private:
    // Controller parameters
    double kp_;
    double ki_;
    double kd_;
    double umin_;
    double umax_;
    double u0_;
    double b_;

    // Signal states
    double u_old_;
    double up_old_;
    double ud_old_;
    double uff_old_;

    // Measurement filter
    MeasurementFilter filter_;
};

#endif // PID_H
