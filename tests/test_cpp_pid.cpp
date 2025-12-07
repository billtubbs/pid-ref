/**
 * @file test_cpp_pid.cpp
 * @brief Unit tests for C++ PID controller
 *
 * Tests the C++ PID controller implementation using the same I/O data
 * CSV files as the Python tests for cross-validation.
 *
 * Uses Catch2 testing framework (v2.x single-header version).
 * Download from: https://github.com/catchorg/Catch2/releases/tag/v2.13.10
 */

#define CATCH_CONFIG_MAIN
#include "catch.hpp"

#include "../cpp_pid/pid.h"
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cmath>

/**
 * @brief Structure to hold controller configuration
 */
struct ControllerConfig {
    std::string description;
    double kp;
    double ki;
    double kd;
    double umin;
    double umax;
};

/**
 * @brief Structure to hold I/O data for one time step
 */
struct IODataRow {
    double r;
    double y;
    double uff;
    double uman;
    double utrack;
    double Tx;
    bool auto_mode;
    bool track;
    double u;  // Expected output
};

/**
 * @brief Parse a boolean value from CSV string
 */
bool parse_bool(const std::string& str) {
    std::string lower = str;
    std::transform(lower.begin(), lower.end(), lower.begin(), ::tolower);
    return (lower == "true");
}

/**
 * @brief Load complete I/O data from CSV file
 *
 * Expected CSV columns: r, y, uff, uman, utrack, Tx, auto, track, u
 *
 * @param filepath Path to CSV file
 * @return Vector of IODataRow structures
 */
std::vector<IODataRow> load_io_data(const std::string& filepath) {
    std::vector<IODataRow> data;
    std::ifstream file(filepath);

    if (!file.is_open()) {
        throw std::runtime_error("Could not open file: " + filepath);
    }

    std::string line;
    // Skip header
    std::getline(file, line);

    // Read data rows
    while (std::getline(file, line)) {
        std::istringstream ss(line);
        std::string token;
        IODataRow row;

        // Parse CSV columns
        std::getline(ss, token, ',');
        row.r = std::stod(token);

        std::getline(ss, token, ',');
        row.y = std::stod(token);

        std::getline(ss, token, ',');
        row.uff = std::stod(token);

        std::getline(ss, token, ',');
        row.uman = std::stod(token);

        std::getline(ss, token, ',');
        row.utrack = std::stod(token);

        std::getline(ss, token, ',');
        row.Tx = std::stod(token);

        std::getline(ss, token, ',');
        row.auto_mode = parse_bool(token);

        std::getline(ss, token, ',');
        row.track = parse_bool(token);

        std::getline(ss, token, ',');
        row.u = std::stod(token);

        data.push_back(row);
    }

    return data;
}

/**
 * @brief Run PID controller test with I/O data
 *
 * @param config Controller configuration
 * @param io_data_file Path to I/O data CSV file
 */
void test_pid_with_io_data(
    const ControllerConfig& config,
    const std::string& io_data_file) {

    // Load I/O data
    std::vector<IODataRow> data = load_io_data(io_data_file);
    REQUIRE(data.size() > 0);

    // Create controller
    PIDController controller(
        config.kp,
        config.ki,
        config.kd,
        10.0,  // TfTs
        config.umin,
        config.umax
    );

    // Run controller with inputs from CSV
    for (size_t i = 0; i < data.size(); ++i) {
        const IODataRow& row = data[i];

        double u = controller(
            row.r,
            row.y,
            row.uff,
            row.uman,
            row.utrack,
            row.Tx,
            row.track,
            row.auto_mode
        );

        // Verify output matches expected value
        // Use relative and absolute tolerance matching Python tests
        double abs_diff = std::abs(u - row.u);
        double rel_diff = std::abs(abs_diff / row.u);

        INFO("Step " << i << ": expected=" << row.u
             << ", actual=" << u << ", diff=" << abs_diff);

        // Check within tolerance (rtol=1e-10, atol=1e-12)
        bool within_tolerance =
            (abs_diff < 1e-12) || (rel_diff < 1e-10);

        REQUIRE(within_tolerance);
    }
}

// Test case definitions matching Python test_cases.yaml
TEST_CASE("P controller with step reference", "[P_step]") {
    ControllerConfig config = {
        "P-only controller",
        1.0,  // kp
        0.0,  // ki
        0.0,  // kd
        -10.0,  // umin
        10.0   // umax
    };

    test_pid_with_io_data(config, "data/P_step.csv");
}

TEST_CASE("PI controller with step reference", "[PI_step]") {
    ControllerConfig config = {
        "PI controller",
        1.0,  // kp
        0.5,  // ki
        0.0,  // kd
        -10.0,  // umin
        10.0   // umax
    };

    test_pid_with_io_data(config, "data/PI_step.csv");
}

TEST_CASE("PID controller with step reference", "[PID_step]") {
    ControllerConfig config = {
        "PID controller",
        1.0,  // kp
        0.5,  // ki
        0.1,  // kd
        -10.0,  // umin
        10.0   // umax
    };

    test_pid_with_io_data(config, "data/PID_step.csv");
}

TEST_CASE("PID with irregular time intervals (adaptive timing)",
          "[PID_step_irregular_time]") {
    ControllerConfig config = {
        "PID controller",
        1.0,  // kp
        0.5,  // ki
        0.1,  // kd
        -10.0,  // umin
        10.0   // umax
    };

    test_pid_with_io_data(config,
                          "data/PID_step_irregular_time.csv");
}

TEST_CASE("PID with saturation (anti-windup)", "[PID_antiwindup_step]") {
    ControllerConfig config = {
        "PID with tight saturation",
        2.0,  // kp
        1.0,  // ki
        0.2,  // kd
        -3.0,  // umin
        3.0   // umax
    };

    test_pid_with_io_data(config, "data/PID_antiwindup_step.csv");
}

TEST_CASE("PI controller with manual mode switching",
          "[PI_switch_manual]") {
    ControllerConfig config = {
        "PI controller",
        1.0,  // kp
        0.5,  // ki
        0.0,  // kd
        -10.0,  // umin
        10.0   // umax
    };

    test_pid_with_io_data(config, "data/PI_switch_manual.csv");
}

TEST_CASE("PI controller with tracking mode", "[PI_switch_track]") {
    ControllerConfig config = {
        "PI controller",
        1.0,  // kp
        0.5,  // ki
        0.0,  // kd
        -10.0,  // umin
        10.0   // umax
    };

    test_pid_with_io_data(config, "data/PI_switch_track.csv");
}
