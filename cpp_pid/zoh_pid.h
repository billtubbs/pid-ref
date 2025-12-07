/**
 * @file zoh_pid.h
 * @brief Zero-order hold (ZOH) discretization for measurement filter
 *
 * This file provides the ZOH discretization function for computing
 * discrete-time filter parameters used in the PID controller's
 * measurement filter.
 */

#ifndef ZOH_PID_H
#define ZOH_PID_H

#include <cmath>

/**
 * @brief Filter parameters structure
 */
struct FilterParams {
    double a11;
    double a12;
    double a21;
    double a22;
    double b1;
    double b2;
};

/**
 * @brief Compute filter parameters using zero-order hold discretization
 *
 * @param TfTs Filter time constant as a multiple of nominal sample time
 * @param Tx Execution period (normalized, default: 1.0)
 * @return FilterParams Structure containing six state-space matrix
 *         coefficients
 */
FilterParams zoh_Fy(double TfTs, double Tx = 1.0);

#endif // ZOH_PID_H
