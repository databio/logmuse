<script>
document.addEventListener('DOMContentLoaded', (event) => {
  document.querySelectorAll('h3 code').forEach((block) => {
    hljs.highlightBlock(block);
  });
});
</script>

<style>
h3 .lucidoc{ 
    padding-left: 22px;
    text-indent: -15px;
 }
h3 .hljs .lucidoc{
    padding-left: 20px;
    margin-left: 0px;
    text-indent: -15px;
    martin-bottom: 0px;
}
h4 .lucidoc, table .lucidoc, p .lucidoc, li .lucidoc { margin-left: 30px; }
h4 .lucidoc { 
    font-style: italic;
    font-size: 1em;
    margin-bottom: 0px;
}

</style>
<div class='lucidoc'>

# Package `logmuse` Documentation

## <a name="AbsentOptionException"></a> Class `AbsentOptionException`
Exception subtype suggesting that client should add log options.


```python
def logger_via_cli(opts, strict=True, **kwargs)
```

Convenience function creating a logger.

This module provides the ability to augment a CLI parser with
logging-related options/arguments so that client applications do not need
intimate knowledge of the implementation. This function completes that
lack of burden, parsing values for the options supplied herein.
#### Parameters:

- `opts` (`argparse.Namespace`):  command-line options/arguments.
- `strict` (`bool`):  whether to raise an exception


#### Returns:

- `logging.Logger`:  configured logger instance.


#### Raises:

- `pararead.logs.AbsentOptionException`:  if one of the expected optionsisn't available in the given Namespace, and the argument to the strict parameter is True. Such a case suggests that a client application didn't use this module to add the expected logging options to a parser.




```python
def setup_logger(name='', level=None, stream=None, logfile=None, make_root=None, propagate=False, silent=False, devmode=False, verbosity=None, fmt=None, datefmt=None, plain_format=False, style=None)
```

Old alias for init_logger for backwards compatibility



```python
def init_logger(name='', level=None, stream=None, logfile=None, make_root=None, propagate=False, silent=False, devmode=False, verbosity=None, fmt=None, datefmt=None, plain_format=False, style=None)
```

Establish and configure primary logger.

This is intended to be called just once per "session", with a "session"
defined as an invocation of the main workflow, a testing session, or an
import of the primary abstractions, e.g. in an interactive iPython session.
#### Parameters:

- `name` (`str`):  name for the logger
- `level` (`int | str`):  minimal level of messages to listen for
- `stream` (`str`):  standard stream to use as log destination. The defaultbehavior is to write logs to stdout, even if null is passed here. This is to allow a CLI argument as input to stream parameter, where it may be undesirable to require specification of a default value in the client application in order to prevent passing None if no CLI option value is given. To disable standard stream logging, set 'silent' to True or pass a path to a file to which to write logs, which gets priority over a standard stream as the destination for log messages.
- `logfile` (`str | FileIO[str]`):  path to filesystem location to use aslogs destination. if provided, this mutes standard stream logging.
- `make_root` (`bool`):  whether to use returned logger as root logger. Thismeans the name will be 'root' and that messages will not propagate.
- `propagate` (`bool`):  whether to allow messages from this logger to reachparent logger(s).
- `silent` (`bool`):  whether to silence logging; this is only guaranteed formessages from this logger and for those from loggers beneath this one in the runtime hierarchy without no separate handling. Propagation must also be turned off separately--if this is not the root logger--in order to ensure that messages are not handled and emitted from a potential parent to the logger built here.
- `devmode` (`bool`):  whether to log in development mode; possibly amongother behavioral changes to logs handling, use a more information-rich message format template.
- `verbosity` (`int | str`):  alternate mode of expression for logging levelthat better accords with intuition about how to convey this. It's positively associated with message volume rather than negatively so, as logging level is. This takes precedence over 'level' if both are present.
- `fmt` (`str`):  message format/template.
- `datefmt` (`str`):  format/template for time component of a log record.
- `plain_format` (`bool`):  force use of plain message format, even ifin development mode (debug level)
- `style` (`str`):  string indicating message formatting strategy; refer tohttps://docs.python.org/3/howto/logging-cookbook.html#use-of-alternative-formatting-styles; only valid in Python3.2+


#### Returns:

- `logging.Logger`:  configured Logger instance


#### Raises:

- `ValueError`:  if attempting to name explicitly non-root logger witha root name, or if both level and verbosity are specified




```python
def add_logging_options(parser)
```

Augment a CLI argument parser with this package's logging options.
#### Parameters:

- `parser` (`argparse.ArgumentParser`):  CLI options and argument parser toaugment with logging options.


#### Returns:

- `argparse.ArgumentParser`:  the input argument, supplemented with thispackage's logging options.




</div>


*Version Information: `logmuse` v0.2.1, generated by `lucidoc` v0.4.0*