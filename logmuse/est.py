"""Project configuration, particularly for logging.

Project-scope constants may reside here, but more importantly, some setup here
will provide a logging infrastructure for all of the project's modules.
Individual modules and classes may provide separate configuration on a more
local level, but this will at least provide a foundation.

"""

import logging
import os
from sys import stdout


LOGGING_LEVEL = "INFO"
LOGGING_LOCATIONS = (stdout, )

# Default user logging format is simple
DEFAULT_LOGGING_FMT = "%(message)s"
# Developer logger format is more information-rich
DEV_LOGGING_FMT = "%(module)s:%(lineno)d (%(funcName)s) [%(levelname)s] > %(message)s "


# Ensure that we have a handler and don't get a logging exception.
# Note that this was originally with looper.models.
_LOGGER = logging.getLogger(__name__)
if not logging.getLogger().handlers:
    _LOGGER.addHandler(logging.NullHandler())


def setup_logger(name, level, additional_locations=None, devmode=False):
    """
    Establish a logger to provide general execution information.\

    :param str name: name for the Logger
    :param int | str level: logging level
    :param tuple(str | FileIO[str]) additional_locations: supplementary
        destination(s) to which to ship logs
    :param bool devmode: whether to use developer logging config
    :return logging.Logger: project-root logger
    """

    logging.addLevelName(5, "VERY_FINE")

    fmt = DEV_LOGGING_FMT if devmode else DEFAULT_LOGGING_FMT

    # Establish the logger.
    logger = logging.getLogger(name)
    # First remove any previously-added handlers
    logger.handlers = []
    logger.propagate = False

    # Handle int- or text-specific logging level.
    try:
        level = int(level)
    except ValueError:
        level = level.upper()

    try:
        logger.setLevel(level)
    except Exception:
        logging.error("Can't set logging level to %s; instead using: '%s'",
                      str(level), str(LOGGING_LEVEL))
        level = LOGGING_LEVEL
        logger.setLevel(level)

    # Process any additional locations.
    locations_exception = None
    where = LOGGING_LOCATIONS
    if additional_locations:
        if isinstance(additional_locations, str):
            additional_locations = (additional_locations, )
        try:
            where = LOGGING_LOCATIONS + tuple(additional_locations)
        except TypeError as e:
            locations_exception = e
    if locations_exception:
        logging.warning(
            "Could not interpret {} as supplementary root logger target "
            "destinations; using {} as root logger location(s)".
            format(additional_locations, LOGGING_LOCATIONS))

    # Add the handlers.
    formatter = logging.Formatter(fmt=(fmt or DEFAULT_LOGGING_FMT))
    for loc in where:
        if isinstance(loc, str):
            # File destination
            dirpath = os.path.abspath(os.path.dirname(loc))
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            handler_type = logging.FileHandler
        elif hasattr(loc, "write"):
            # Stream destination
            handler_type = logging.StreamHandler
        else:
            # Strange supplementary destination
            logging.info("{} as logs destination appears to be neither "
                         "a filepath nor a stream.".format(loc))
            continue

        if handler_type is logging.FileHandler:
            handler = handler_type(loc, mode='w')
        else:
            handler = handler_type(loc)

        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
