# Guessing Game (From the official Maturin document)
> https://www.maturin.rs/tutorial.html

## Scaffold the Project

Initialize a new project using PyO3 bindings:

```bash
maturin init -b pyo3
```

## Set Up a Virtual Environment

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Development

Build and install the module into the active Python environment:

```bash
maturin develop
```

## Running the Module in Python

Start a Python REPL and import the module:

```python
python
>>> import guessing_game
>>> guessing_game.guess_the_number()
```

## Building the Package

Build a distributable Python wheel:

```bash
maturin build
```

The generated wheel will be placed in:

```
target/wheels/
```
