# Greet in Rust 

This project implements a high-performance Python greeting library using Rust.

It uses a decoupled architecture to keep the Python source tree clean of compilation artifacts (like `.so` or `.dSYM` files).

## Project Structure

* `crates/greet`: Core Rust logic (compiled as an `rlib`).
* `py-greet/runtime/`: The `maturin` bridge that generates the binary.
* `py-greet/src/`: Pure Python API and user-facing code.

## Getting Started

### 1. Environment Setup

Initialize your virtual environment and install the necessary build and testing tools.

```bash
# Create and activate venv
python3 -m venv .venv
source .venv/bin/activate

# Install essential tools
pip install --upgrade pip
pip install setuptools pytest
```

### 2. Build & Install the Runtime

This step compiles the Rust code and installs the binary module into your virtual environment. Because we use `maturin develop`, the binary is managed by the venv and won't clutter your `src` folder.

```bash
cd py-greet/runtime/greet-runtime
maturin develop
```

### 3. Install the Python API

Install the main `py-greet` package in editable mode. This links your Python source code so changes are reflected immediately.

```bash
cd py-greet
pip install -e .
```

##  Running Tests

Since the runtime is installed in your `.venv` and the package is installed in editable mode, you can run tests from the root or the `py-greet` folder.

```bash
# Ensure venv is active
source .venv/bin/activate

# Run all tests
pytest py-greet/tests
```

## Maintenance

### Cleaning Artifacts

If you need to wipe the build cache or temporary Python files:

```bash
# Clean Rust build artifacts
cargo clean

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
```

### Development Workflow

1. Modify Rust logic in `crates/greet/src`.
2. Re-run `maturin develop` inside `py-greet/runtime/greet-runtime`.
3. Modify Python logic in `py-greet/src/greet`.
4. Run `pytest`.
