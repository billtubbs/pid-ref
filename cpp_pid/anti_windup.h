/**
 * @file anti_windup.h
 * @brief Anti-windup logic for the PID controller integral term
 *
 * This file provides functionality to prevent integrator windup when
 * the control signal is saturated.
 */

#ifndef ANTI_WINDUP_H
#define ANTI_WINDUP_H

/**
 * @brief Windup mode enumeration
 */
enum class WindupMode {
    NONE,
    UPPER,
    LOWER,
    BOTH
};

/**
 * @brief Apply anti-windup logic to the integral increment
 *
 * Prevents the integrator from accumulating error when the control
 * signal is saturated by restricting integration in the direction
 * of saturation.
 *
 * @param Dui Integral control signal increment
 * @param windup Windup status indicating which limit(s) are active
 * @return Modified integral increment that respects saturation
 *         constraints
 */
double anti_windup(double Dui, WindupMode windup);

/**
 * @brief Convenience function for no windup
 */
inline double anti_windup(double Dui) {
    return anti_windup(Dui, WindupMode::NONE);
}

#endif // ANTI_WINDUP_H
