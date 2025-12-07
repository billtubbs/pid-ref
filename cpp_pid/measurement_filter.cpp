/**
 * @file measurement_filter.cpp
 * @brief Implementation of measurement filter
 */

#include "measurement_filter.h"

MeasurementFilter::MeasurementFilter(double TfTs)
    : TfTs_(TfTs),
      a11_(0.0),
      a12_(0.0),
      a21_(0.0),
      a22_(0.0),
      b1_(0.0),
      b2_(0.0),
      yf_(0.0),
      dyf_(0.0),
      Tx_old_(std::numeric_limits<double>::quiet_NaN()),
      initialized_(false) {}

FilterOutput MeasurementFilter::operator()(double y, double Tx) {
    // Rediscretize to match execution period
    if (!initialized_ || Tx != Tx_old_) {
        FilterParams params = zoh_Fy(TfTs_, Tx);
        a11_ = params.a11;
        a12_ = params.a12;
        a21_ = params.a21;
        a22_ = params.a22;
        b1_ = params.b1;
        b2_ = params.b2;
        initialized_ = true;
    }

    // State update
    double yf_prev = yf_;
    Tx_old_ = Tx;
    yf_ = a11_ * yf_prev + a12_ * dyf_ + b1_ * y;
    dyf_ = a21_ * yf_prev + a22_ * dyf_ + b2_ * y;

    FilterOutput output;
    output.yf = yf_;
    output.dyf = dyf_;
    return output;
}

void MeasurementFilter::reset() {
    yf_ = 0.0;
    dyf_ = 0.0;
    Tx_old_ = std::numeric_limits<double>::quiet_NaN();
    initialized_ = false;
}
