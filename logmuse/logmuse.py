"""Project logging configuration."""

import argparse
import logging
import os
import sys
import warnings
from importlib.metadata import version
from typing import IO

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"

__all__ = [
    "add_logging_options",
    "logger_via_cli",
    "init_logger",
    "setup_logger",
    "AbsentOptionException",
    "LOGGING_CLI_OPTDATA",
]


BASIC_LOGGING_FORMAT: str = "%(message)s"
DEV_LOGGING_FMT: str = (
    "%(levelname).4s %(asctime)s | %(name)s:%(module)s:%(lineno)d > %(message)s "
)
FULL_DEV_LOGGING_FMT: str = (
    "%(levelname)s %(asctime)s | %(name)s:%(module)s:%(lineno)d > %(message)s "
)
DEFAULT_DATE_FMT: str = "%H:%M:%S"
PACKAGE_NAME: str = "logmuse"
STREAMS: dict[str, IO] = {"OUT": sys.stdout, "ERR": sys.stderr}
DEFAULT_STREAM: IO = STREAMS["ERR"]
LOGGING_LEVEL: str = "INFO"
LOGGING_LOCATIONS: tuple[IO, ...] = (DEFAULT_STREAM,)
TRACE_LEVEL_VALUE: int = 5
TRACE_LEVEL_NAME: str = "TRACE"
CUSTOM_LEVELS: dict[str, int] = {TRACE_LEVEL_NAME: TRACE_LEVEL_VALUE}
SILENCE_LOGS_OPTNAME: str = "silent"
VERBOSITY_OPTNAME: str = "verbosity"
DEVMODE_OPTNAME: str = "logdev"
PARAM_BY_OPTNAME: dict[str, str] = {DEVMODE_OPTNAME: "devmode"}

# Translation of verbosity into logging level.
# Log message count monotonically increases in verbosity while it decreases
# in logging level, making verbosity a more intuitive specification mechanism.
_WARN_REPR: str = "WARN"
LEVEL_BY_VERBOSITY: list[str] = ["CRITICAL", "ERROR", _WARN_REPR, "INFO", "DEBUG"]
_MIN_VERBOSITY: int = 1
_MAX_VERBOSITY: int = len(LEVEL_BY_VERBOSITY)
_VERBOSITY_CHOICES: list[str] = (
    [str(x) for x in range(_MIN_VERBOSITY, len(LEVEL_BY_VERBOSITY) + 1)]
    + LEVEL_BY_VERBOSITY
    + ["WARNING"]
)

LOGGING_CLI_OPTDATA: dict[str, dict] = {
    SILENCE_LOGS_OPTNAME: {
        "action": "store_true",
        "help": "Silence logging. Overrides {}.".format(VERBOSITY_OPTNAME),
    },
    VERBOSITY_OPTNAME: {
        "metavar": "V",
        "choices": _VERBOSITY_CHOICES,
        "help": "Set logging level ({}-{} or logging module level name)".format(
            _MIN_VERBOSITY, len(LEVEL_BY_VERBOSITY)
        ),
    },
    DEVMODE_OPTNAME: {
        "action": "store_true",
        "help": "Expand content of logging message format.",
    },
}


def add_logging_options(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Augment a CLI argument parser with this package's logging options.

    Args:
        parser: CLI options and argument parser to augment with logging options.

    Returns:
        The input argument, supplemented with this package's logging options.
    """
    for optname, optdata in LOGGING_CLI_OPTDATA.items():
        parser.add_argument("--{}".format(optname), **optdata)
    return parser


def logger_via_cli(
    opts: argparse.Namespace, strict: bool = True, **kwargs
) -> logging.Logger:
    """Convenience function creating a logger from parsed CLI options.

    This module provides the ability to augment a CLI parser with
    logging-related options/arguments so that client applications do not need
    intimate knowledge of the implementation. This function completes that
    lack of burden, parsing values for the options supplied herein.

    Args:
        opts: Command-line options/arguments.
        strict: Whether to raise an exception if expected options are missing.
        **kwargs: Additional keyword arguments passed to init_logger.

    Returns:
        Configured logger instance.

    Raises:
        AbsentOptionException: If one of the expected options isn't available
            in the given Namespace, and strict is True.
    """
    logs_cli_args = {}
    for optname in LOGGING_CLI_OPTDATA.keys():
        name = optname.lstrip("-")
        try:
            optval = getattr(opts, name)
        except AttributeError:
            if strict:
                raise AbsentOptionException(optname)
            continue
        else:
            logs_cli_args[PARAM_BY_OPTNAME.get(optname, name)] = optval
    logs_cli_args.update(kwargs)
    return init_logger(**logs_cli_args)


def init_logger(
    name: str = "",
    level: int | str | None = None,
    stream: str | IO | None = None,
    logfile: str | None = None,
    logfile_mode: str = "a",
    make_root: bool | None = None,
    propagate: bool = False,
    silent: bool = False,
    devmode: bool = False,
    verbosity: int | str | None = None,
    fmt: str | None = None,
    datefmt: str = DEFAULT_DATE_FMT,
    plain_format: bool = False,
    style: str | None = None,
    use_full_names: bool = False,
) -> logging.Logger:
    """Establish and configure primary logger.

    This is intended to be called just once per "session", with a "session"
    defined as an invocation of the main workflow, a testing session, or an
    import of the primary abstractions, e.g. in an interactive iPython session.

    Args:
        name: Name for the logger.
        level: Minimal level of messages to listen for.
        stream: Standard stream to use as log destination. The default
            behavior is to write logs to stderr, even if None is passed here.
            To disable standard stream logging, set 'silent' to True or pass
            a path to a file via logfile.
        logfile: Path to filesystem location to use as logs destination.
            If provided, this mutes standard stream logging.
        logfile_mode: File open mode for logfile. Default is "a" (append).
            Use "w" to overwrite.
        make_root: Whether to use returned logger as root logger.
        propagate: Whether to allow messages from this logger to reach
            parent logger(s).
        silent: Whether to silence logging.
        devmode: Whether to log in development mode; uses a more
            information-rich message format template.
        verbosity: Alternate mode of expression for logging level that is
            positively associated with message volume. Takes precedence
            over 'level' if both are present.
        fmt: Message format/template.
        datefmt: Format/template for time component of a log record.
        plain_format: Force use of plain message format, even if in
            development mode.
        style: String indicating message formatting strategy.
        use_full_names: Don't truncate level names.

    Returns:
        Configured Logger instance.

    Raises:
        ValueError: If attempting to name explicitly non-root logger with
            a root name, or if both level and verbosity are specified.
    """
    if make_root is True:
        if propagate:
            logging.warning("Propagation from root logger is nonsense")
        if name and name != "root":
            logging.warning("Requested root logger with non-root name: {}".format(name))
    else:
        name = name or PACKAGE_NAME
        if make_root is False and name == "root":
            raise ValueError(
                "Requested non-root logger with root name: {}".format(name)
            )

    # Enable named ultrafine logging for debugging.
    for level_name, level_value in CUSTOM_LEVELS.items():
        logging.addLevelName(level_value, level_name)

    # Establish the logger.
    logger = logging.getLogger(name)
    logger.handlers = []
    logger.propagate = propagate

    # Either short-circuit with a silent logger or parse and set level.
    if silent:
        logger.addHandler(logging.NullHandler())
        return logger

    # Determine the logger's listening level.
    if level is not None and verbosity is not None:
        raise ValueError(
            "Cannot specify both level and verbosity; got {} and "
            "{}, respectively".format(level, verbosity)
        )
    elif level is not None:
        try:
            level = int(level)
        except ValueError:
            level = level.upper()
    else:
        level = _level_from_verbosity(verbosity or LOGGING_LEVEL)
    try:
        level = getattr(logging, level) if isinstance(level, str) else level
        logger.setLevel(level)
    except Exception:
        logging.error(
            "Can't set logging level to %s; instead using: '%s'",
            str(level),
            str(LOGGING_LEVEL),
        )
        level = LOGGING_LEVEL
        logger.setLevel(level)

    handlers = []

    if logfile:
        logfile_folder = os.path.dirname(logfile)
        if not os.path.exists(logfile_folder):
            os.makedirs(logfile_folder)
        handlers.append(logging.FileHandler(logfile, mode=logfile_mode))
    if stream or not logfile:
        if not stream:
            stream = DEFAULT_STREAM
            stream_loc = stream
        elif stream in [sys.stderr, sys.stdout]:
            stream_loc = stream
        else:
            try:
                stream_loc = STREAMS[stream.upper()]
            except (AttributeError, KeyError):
                print(
                    "Invalid stream location: {}; using {}".format(
                        stream, DEFAULT_STREAM
                    )
                )
                stream_loc = DEFAULT_STREAM
        handlers.append(logging.StreamHandler(stream_loc))

    fine = level <= logging.DEBUG
    get_fmt = (
        (lambda _: fmt)
        if fmt
        else (
            lambda hdlr: (
                BASIC_LOGGING_FORMAT
                if plain_format
                or not (devmode or fine or isinstance(hdlr, logging.FileHandler))
                else (FULL_DEV_LOGGING_FMT if use_full_names else DEV_LOGGING_FMT)
            )
        )
    )

    fmt_kwargs: dict[str, str] = {"datefmt": datefmt}
    if style:
        fmt_kwargs["style"] = style

    for h in handlers:
        h.setFormatter(logging.Formatter(get_fmt(h), **fmt_kwargs))
        h.setLevel(level)
        logger.addHandler(h)

    # If coloredlogs is installed, colorize stream handlers.
    try:
        import coloredlogs

        for h in handlers:
            if isinstance(h, logging.StreamHandler) and not isinstance(
                h, logging.FileHandler
            ):
                coloredlogs.install(
                    level=level,
                    logger=logger,
                    stream=h.stream,
                    fmt=get_fmt(h),
                    **fmt_kwargs,
                )
                break
    except ImportError:
        pass

    logger.debug(
        "Configured logger '%s' using %s v%s",
        logger.name,
        PACKAGE_NAME,
        version(PACKAGE_NAME),
    )

    return logger


def setup_logger(
    name: str = "",
    level: int | str | None = None,
    stream: str | IO | None = None,
    logfile: str | None = None,
    logfile_mode: str = "a",
    make_root: bool | None = None,
    propagate: bool = False,
    silent: bool = False,
    devmode: bool = False,
    verbosity: int | str | None = None,
    fmt: str | None = None,
    datefmt: str = DEFAULT_DATE_FMT,
    plain_format: bool = False,
    style: str | None = None,
    use_full_names: bool = False,
) -> logging.Logger:
    """Old alias for init_logger for backwards compatibility."""
    warnings.warn("Please use init_logger in place of setup_logger", DeprecationWarning)
    return init_logger(
        name,
        level,
        stream,
        logfile,
        logfile_mode,
        make_root,
        propagate,
        silent,
        devmode,
        verbosity,
        fmt,
        datefmt,
        plain_format,
        style,
        use_full_names,
    )


def _level_from_verbosity(verbosity: int | str) -> int | str:
    """Translate verbosity into logging level.

    Log message count monotonically increases in verbosity while it decreases
    in logging level, making verbosity a more intuitive specification mechanism.

    Args:
        verbosity: Small integral value representing a relative measure of
            interest in seeing messages, or the name of a Python builtin
            logging level.

    Returns:
        Numeric logging level in accordance with Python builtin logging.

    Raises:
        ValueError: If the verbosity string is not a recognized level.
        TypeError: If verbosity is neither a string nor an int.
    """
    try:
        verbosity = int(verbosity)
    except (ValueError, TypeError):
        pass
    if isinstance(verbosity, str):
        v = verbosity.upper()
        if v.startswith(_WARN_REPR):
            v = _WARN_REPR
        if v not in LEVEL_BY_VERBOSITY:
            raise ValueError(
                "Invalid logging verbosity ('{}'); choose from: {}".format(
                    verbosity, ", ".join(LEVEL_BY_VERBOSITY)
                )
            )
        return getattr(logging, v)
    elif isinstance(verbosity, int):
        return LEVEL_BY_VERBOSITY[verbosity - 1]  # 1-based user, 0-based internal
    else:
        raise TypeError(
            "Verbosity must be string or int; got {} ({})".format(
                verbosity, type(verbosity)
            )
        )


class AbsentOptionException(Exception):
    """Exception subtype suggesting that client should add log options."""

    def __init__(self, missing_optname: str) -> None:
        likely_reason = (
            "'{}' not in the parsed options; was {} used to "
            "add CLI logging options to an argument parser?".format(
                missing_optname, "{}.{}".format(__name__, add_logging_options.__name__)
            )
        )
        super().__init__(likely_reason)


def get_logger(name: str) -> logging.Logger:
    """Return a logger with given name, equipped with custom method.

    Args:
        name: Name for the logger to get/create.

    Returns:
        Named, custom logger instance.
    """
    lgr = logging.getLogger(name)
    lgr.whisper = lambda msg, *args, **kwargs: lgr.log(5, msg, *args, **kwargs)
    return lgr
