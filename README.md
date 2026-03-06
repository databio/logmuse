# logmuse

[![Build Status](https://github.com/databio/logmuse/actions/workflows/run-pytest.yml/badge.svg?branch=master)](https://github.com/databio/logmuse/actions/workflows/run-pytest.yml)

A small Python package that makes it easy to add CLI-controllable logging to your command-line tools. It provides a simple interface for standard logging arguments (`--verbosity`, `--silent`, `--logdev`) that can be passed directly to a logger.

## Installation

```bash
pip install logmuse
```

## Quick start

Add logging options to your CLI and create a logger in three lines:

```python
import argparse
import logmuse

parser = argparse.ArgumentParser()
# your arguments here...
parser = logmuse.add_logging_options(parser)
args = parser.parse_args()
logger = logmuse.logger_via_cli(args)

logger.info("Hello, world!")
```

This adds `--silent`, `--verbosity`, and `--logdev` options to your CLI automatically.

## Setup for a CLI package

### 1. Initialize in `__init__.py`

```python
import logmuse
logmuse.init_logger("my_package")
```

This sets up default logging parameters for within-Python use. Only do this in the CLI package, not in imported library packages.

### 2. Add CLI args to your argparser

```python
parser = logmuse.add_logging_options(parser)
```

This gives you `--verbosity`, `--silent`, and `--logdev` options.

### 3. Activate in your main function

```python
import logmuse

def main():
    # ... parse args ...
    global _LOGGER
    _LOGGER = logmuse.logger_via_cli(args, make_root=True)
```

### For imported packages

Imported packages don't need logmuse at all. Just use the standard `logging` module:

```python
import logging
_LOGGER = logging.getLogger(__name__)
```

The CLI arguments passed to logmuse will control these loggers too.

## Using logmuse interactively

To set logging to DEBUG in an interactive session:

```python
logmuse.init_logger("my_package", "DEBUG", devmode=True)
```

## Usage reference

### CLI options

`add_logging_options(parser)` adds three arguments to an `argparse.ArgumentParser`:

| Option | Effect |
|---|---|
| `--silent` | Silence all logging output |
| `--verbosity V` | Set logging level (1=CRITICAL, 2=ERROR, 3=WARN, 4=INFO, 5=DEBUG, or a level name) |
| `--logdev` | Use a detailed developer log format with timestamps, module, and line numbers |

### `init_logger` parameters

| Parameter | Default | Description |
|---|---|---|
| `name` | `"logmuse"` | Logger name |
| `level` | `None` | Logging level (int or string) |
| `verbosity` | `None` | Verbosity level (1-5); alternative to `level` |
| `silent` | `False` | Silence all output |
| `devmode` | `False` | Use detailed developer format |
| `stream` | `stderr` | Output stream (`"OUT"` for stdout, `"ERR"` for stderr) |
| `logfile` | `None` | Path to log file (mutes stream output) |
| `make_root` | `None` | Use as root logger |
| `propagate` | `False` | Allow messages to reach parent loggers |
| `fmt` | `None` | Custom format string |
| `datefmt` | `"%H:%M:%S"` | Time format |
| `plain_format` | `False` | Force plain format even in devmode |
| `style` | `None` | Format style (`%`, `{`, or `$`) |
| `use_full_names` | `False` | Don't truncate level names |

### Verbosity levels

| Verbosity | Logging Level |
|---|---|
| 1 | CRITICAL |
| 2 | ERROR |
| 3 | WARN |
| 4 | INFO |
| 5 | DEBUG |
