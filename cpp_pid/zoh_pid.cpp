/**
 * @file zoh_pid.cpp
 * @brief Implementation of ZOH discretization for measurement filter
 */

#include "zoh_pid.h"

FilterParams zoh_Fy(double TfTs, double Tx) {
    // Help variables
    double h1 = Tx / TfTs;
    double h2 = exp(-h1);
    double h3 = h1 * h2;
    double h4 = h3 / TfTs;

    // Filter parameters
    FilterParams params;
    params.a11 = h2 + h3;
    params.a12 = h2;
    params.a21 = -h4;
    params.a22 = h2 - h3;
    params.b1 = 1.0 - h2 - h3;
    params.b2 = h4;

    return params;
}
