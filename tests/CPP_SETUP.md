# C++ Tests Setup Guide for VS Code on macOS

This guide shows you how to compile and run the C++ PID controller tests in VS Code.

## Prerequisites

1. **Xcode Command Line Tools** (provides clang++ compiler):
   ```bash
   xcode-select --install
   ```

2. **VS Code Extensions** (install via Extensions panel):
   - C/C++ (by Microsoft)
   - C/C++ Extension Pack (by Microsoft)

## Quick Setup

Run the automated setup script:

```bash
cd tests
./setup_cpp_tests.sh
```

This will:
- Download Catch2 test framework header
- Generate I/O data files if needed
- Show next steps

## Manual Setup

If you prefer to set up manually:

### 1. Download Catch2

```bash
cd tests
curl -L -o catch.hpp https://github.com/catchorg/Catch2/releases/download/v2.13.10/catch.hpp
```

### 2. Generate Test Data

```bash
cd tests
python3 generate_io_data.py
```

## Building and Running Tests

### Option 1: Using VS Code Tasks (Recommended)

**Build:**
- Press `Cmd+Shift+B` (or Terminal → Run Build Task)
- Select "Build C++ Tests"

**Run Tests:**
- Press `Cmd+Shift+P`
- Type "Tasks: Run Test Task"
- Select "Run C++ Tests"

**Run with Verbose Output:**
- Press `Cmd+Shift+P`
- Type "Tasks: Run Task"
- Select "Run C++ Tests (Verbose)"

**Clean Build:**
- Press `Cmd+Shift+P`
- Type "Tasks: Run Task"
- Select "Clean C++ Build"

### Option 2: Using Integrated Terminal

```bash
cd tests

# Build
make

# Run tests
make test

# Run with verbose output
make test-verbose

# Clean build artifacts
make clean
```

### Option 3: Using Debugger

1. Set breakpoints in `test_cpp_pid.cpp` or C++ source files
2. Press `F5` (or Run → Start Debugging)
3. Select "Debug C++ Tests"

The debugger will:
- Automatically build the tests
- Run with breakpoints enabled
- Stop at any failures or breakpoints

## VS Code Configuration Files

The following files have been created in `.vscode/`:

- **c_cpp_properties.json** - IntelliSense configuration
- **tasks.json** - Build and run tasks
- **launch.json** - Debugging configuration

These enable:
- Code completion and IntelliSense
- Error checking
- One-click build/run/debug
- Integrated terminal output

## Troubleshooting

### "catch.hpp not found"

Run the setup script or manually download:
```bash
cd tests
curl -L -o catch.hpp https://github.com/catchorg/Catch2/releases/download/v2.13.10/catch.hpp
```

### "No such file or directory: data/*.csv"

Generate I/O data:
```bash
python3 tests/generate_io_data.py
```

### "clang: error: unknown argument"

Make sure you have Xcode Command Line Tools:
```bash
xcode-select --install
```

### Build errors about missing headers

Check IntelliSense configuration:
1. Open Command Palette (`Cmd+Shift+P`)
2. Type "C/C++: Edit Configurations (UI)"
3. Verify include paths contain:
   - `${workspaceFolder}/cpp_pid`
   - `${workspaceFolder}/tests`

### Tests fail with "file not found"

Make sure you run from the `tests` directory or use the VS Code tasks which set the correct working directory.

## Running Specific Tests

To run only specific test cases, use Catch2 tags:

```bash
# Run only P_step test
./test_cpp_pid "[P_step]"

# Run only manual switching tests
./test_cpp_pid "[PI_switch_manual]"

# Run all except tracking tests
./test_cpp_pid "~[PI_switch_track]"
```

## VS Code Keyboard Shortcuts

- `Cmd+Shift+B` - Build
- `F5` - Start debugging
- `Shift+F5` - Stop debugging
- `F9` - Toggle breakpoint
- `F10` - Step over
- `F11` - Step into
- `Shift+F11` - Step out

## Next Steps

- Modify test cases in `test_cpp_pid.cpp`
- Add new controller configurations
- Create custom I/O data files
- Implement additional features in `cpp_pid/`
