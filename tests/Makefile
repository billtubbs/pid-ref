# Makefile for C++ PID controller tests
# Requires Catch2 v2.x single-header file (catch.hpp)

CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -I. -I..
LDFLAGS = -lm

# Source files
CPP_PID_DIR = ../cpp_pid
CPP_PID_SOURCES = \
	$(CPP_PID_DIR)/zoh_pid.cpp \
	$(CPP_PID_DIR)/anti_windup.cpp \
	$(CPP_PID_DIR)/measurement_filter.cpp \
	$(CPP_PID_DIR)/pid.cpp

TEST_SOURCES = test_cpp_pid.cpp
TEST_TARGET = test_cpp_pid

# Object files
CPP_PID_OBJECTS = $(CPP_PID_SOURCES:.cpp=.o)
TEST_OBJECTS = $(TEST_SOURCES:.cpp=.o)

.PHONY: all clean test help

all: $(TEST_TARGET)

$(TEST_TARGET): $(CPP_PID_OBJECTS) $(TEST_OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

test: $(TEST_TARGET)
	./$(TEST_TARGET)

test-verbose: $(TEST_TARGET)
	./$(TEST_TARGET) -s

clean:
	rm -f $(CPP_PID_OBJECTS) $(TEST_OBJECTS) $(TEST_TARGET)

help:
	@echo "C++ PID Controller Test Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  make          - Build test executable"
	@echo "  make test     - Build and run tests"
	@echo "  make test-verbose - Run tests with detailed output"
	@echo "  make clean    - Remove build artifacts"
	@echo ""
	@echo "Prerequisites:"
	@echo "  1. Download catch.hpp (Catch2 v2.x single-header)"
	@echo "     wget https://github.com/catchorg/Catch2/releases/download/v2.13.10/catch.hpp"
	@echo "  2. Place catch.hpp in tests/ directory"
	@echo "  3. Generate I/O data: python3 tests/generate_io_data.py"
	@echo "  4. Run: make test"
