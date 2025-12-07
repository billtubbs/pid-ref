/**
 * @file measurement_filter.h
 * @brief Measurement filter for PID controller
 *
 * This file provides a second-order filter for filtering the process
 * measurement and computing its filtered derivative for use in the
 * D-term of the PID controller.
 */

#ifndef MEASUREMENT_FILTER_H
#define MEASUREMENT_FILTER_H

#include "zoh_pid.h"
#include <limits>

/**
 * @brief Measurement filter output structure
 */
struct FilterOutput {
    double yf;   ///< Filtered output
    double dyf;  ///< Filtered derivative
};

/**
 * @brief Second-order measurement filter with automatic
 *        re-discretization
 *
 * The filter provides both filtered output and filtered derivative,
 * with automatic parameter adjustment when the execution period
 * changes.
 */
class MeasurementFilter {
public:
    /**
     * @brief Constructor
     *
     * @param TfTs Filter time constant as a multiple of nominal sample
     *             time (default: 10.0)
     */
    explicit MeasurementFilter(double TfTs = 10.0);

    /**
     * @brief Apply the filter to a measurement
     *
     * @param y Process measurement
     * @param Tx Execution period (normalized, default: 1.0)
     * @return FilterOutput containing filtered output and derivative
     */
    FilterOutput operator()(double y, double Tx = 1.0);

    /**
     * @brief Reset the filter state to zero
     */
    void reset();

private:
    // Filter time constant parameter
    double TfTs_;

    // Filter parameters
    double a11_;
    double a12_;
    double a21_;
    double a22_;
    double b1_;
    double b2_;

    // Filter state
    double yf_;
    double dyf_;
    double Tx_old_;

    // Flag to track if filter has been initialized
    bool initialized_;
};

#endif // MEASUREMENT_FILTER_H
