/**
 * @file anti_windup.cpp
 * @brief Implementation of anti-windup logic
 */

#include "anti_windup.h"
#include <algorithm>

double anti_windup(double Dui, WindupMode windup) {
    // Prevent increase, decrease, or both
    if (windup == WindupMode::BOTH || windup == WindupMode::LOWER) {
        Dui = std::max(Dui, 0.0);
    }

    if (windup == WindupMode::BOTH || windup == WindupMode::UPPER) {
        Dui = std::min(Dui, 0.0);
    }

    return Dui;
}
