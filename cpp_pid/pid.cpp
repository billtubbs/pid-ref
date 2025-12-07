/**
 * @file pid.cpp
 * @brief Implementation of PID controller
 */

#include "pid.h"
#include <algorithm>

PIDController::PIDController(
    double kp,
    double ki,
    double kd,
    double TfTs,
    double umin,
    double umax,
    double u0,
    double b)
    : kp_(kp),
      ki_(ki),
      kd_(kd),
      umin_(umin),
      umax_(umax),
      u0_(u0),
      b_(b),
      u_old_(0.0),
      up_old_(0.0),
      ud_old_(0.0),
      uff_old_(0.0),
      filter_(TfTs) {}

double PIDController::operator()(
    double r,
    double y,
    double uff,
    double uman,
    double utrack,
    double Tx,
    bool track,
    bool auto_mode,
    WindupMode windup) {

    // Filter updates
    FilterOutput filtered = filter_(y, Tx);
    double yf = filtered.yf;
    double dyf = filtered.dyf;

    double u;

    if (auto_mode) {
        // Reset state if using P or PD control (ki == 0)
        if (ki_ == 0.0) {
            u_old_ = u0_;  // Bias term if P or PD control
            up_old_ = 0.0;
            ud_old_ = 0.0;
            uff_old_ = 0.0;
            b_ = 1.0;
        }

        // Tracking mode for bumpless transfer
        if (track) {
            u_old_ = utrack;
            up_old_ = 0.0;
            ud_old_ = 0.0;
            uff_old_ = 0.0;
        }

        // Control signal increments
        double Dup = kp_ * (b_ * r - yf) - up_old_;
        double Dui = ki_ * (r - yf) * Tx;
        Dui = anti_windup(Dui, windup);
        double Dud = (-kd_ * dyf - ud_old_) / Tx;
        double Duff = uff - uff_old_;

        // Add control signal increment
        double Du = Dup + Dui + Dud + Duff;
        u = u_old_ + Du;
    } else {
        // Manual control signal
        u = uman;
    }

    // Saturate control signal
    u = std::max(std::min(u, umax_), umin_);

    // Update old signal states
    u_old_ = u;
    up_old_ = kp_ * (b_ * r - yf);
    ud_old_ = -kd_ * dyf;
    uff_old_ = uff;

    return u;
}

void PIDController::reset() {
    u_old_ = 0.0;
    up_old_ = 0.0;
    ud_old_ = 0.0;
    uff_old_ = 0.0;
    filter_.reset();
}
