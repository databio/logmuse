# Package logmuse Documentation

## Class AbsentOptionException
Exception subtype suggesting that client should add log options.


### add\_logging\_options
Augment a CLI argument parser with this package's logging options.
```python
def add_logging_options(parser)
```

**Parameters:**

- `parser` -- `argparse.ArgumentParser`:  CLI options and argument parser toaugment with logging options.


**Returns:**

`argparse.ArgumentParser`:  the input argument, supplemented with thispackage's logging options.




### logger\_via\_cli
Convenience function creating a logger.

This module provides the ability to augment a CLI parser with
logging-related options/arguments so that client applications do not need
intimate knowledge of the implementation. This function completes that
lack of burden, parsing values for the options supplied herein.
```python
def logger_via_cli(opts, **kwargs)
```

**Parameters:**

- `opts` -- `argparse.Namespace`:  command-line options/arguments.


**Returns:**

`logging.Logger`:  configured logger instance.


**Raises:**

- `pararead.logs.AbsentOptionException`:  if one of the expected optionsisn't available in the given Namespace. Such a case suggests that a client application didn't use this module to add the expected logging options to a parser.




### setup\_logger
Establish and configure primary logger.

This is intended to be called just once per "session", with a "session"
defined as an invocation of the main workflow, a testing session, or an
import of the primary abstractions, e.g. in an interactive iPython session.
```python
def setup_logger(name='', level=None, stream=None, logfile=None, make_root=None, propagate=False, silent=False, devmode=False, verbosity=None, fmt=None, datefmt=None, plain_format=False)
```

**Parameters:**

- `name` -- `str`:  name for the logger
- `level` -- `int | str`:  minimal level of messages to listen for
- `stream` -- `str`:  standard stream to use as log destination. The defaultbehavior is to write logs to stdout, even if null is passed here. This is to allow a CLI argument as input to stream parameter, where it may be undesirable to require specification of a default value in the client application in order to prevent passing None if no CLI option value is given. To disable standard stream logging, set 'silent' to True or pass a path to a file to which to write logs, which gets priority over a standard stream as the destination for log messages.
- `logfile` -- `str | FileIO[str]`:  path to filesystem location to use aslogs destination. if provided, this mutes standard stream logging.
- `make_root` -- `bool`:  whether to use returned logger as root logger. Thismeans the name will be 'root' and that messages will not propagate.
- `propagate` -- `bool`:  whether to allow messages from this logger to reachparent logger(s).
- `silent` -- `bool`:  whether to silence logging; this is only guaranteed formessages from this logger and for those from loggers beneath this one in the runtime hierarchy without no separate handling. Propagation must also be turned off separately--if this is not the root logger--in order to ensure that messages are not handled and emitted from a potential parent to the logger built here.
- `devmode` -- `bool`:  whether to log in development mode; possibly amongother behavioral changes to logs handling, use a more information-rich message format template.
- `verbosity` -- `int | str`:  alternate mode of expression for logging levelthat better accords with intuition about how to convey this. It's positively associated with message volume rather than negatively so, as logging level is. This takes precedence over 'level' if both are present.
- `fmt` -- `str`:  message format/template.
- `datefmt` -- `str`:  format/template for time component of a log record.
- `plain_format` -- `bool`:  force use of plain message format, even ifin development mode (debug level)


**Returns:**

`logging.Logger`:  configured Logger instance


**Raises:**

- `ValueError`:  if attempting to name explicitly non-root logger witha root name, or if both level and verbosity are specified



