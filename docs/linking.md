# How to link logmuse loggers

```
# Set the logging level.
if args.dbg:
    # Debug mode takes precedence and will listen for all messages.
    level = args.logging_level or logging.DEBUG
elif args.verbosity is not None:
    # Verbosity-framed specification trumps logging_level.
    level = _LEVEL_BY_VERBOSITY[args.verbosity]
else:
    # Normally, we're not in debug mode, and there's not verbosity.
    level = LOGGING_LEVEL

# Establish the project-root logger and attach one for this module.
logger_kwargs = {"level": level, "logfile": args.logfile, "devmode": args.dbg}
init_logger(name="peppy", **logger_kwargs)
init_logger(name="divvy", **logger_kwargs)
global _LOGGER
_LOGGER = init_logger(name=_PKGNAME, **logger_kwargs)


logger_kwargs = {"level": level, "logfile": args.logfile, "devmode": args.dbg}
init_logger(name="peppy", **logger_kwargs)
init_logger(name="divvy", **logger_kwargs)
```

Should move the logging level stuff into logmuse