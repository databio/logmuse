# Tutorial

## Client packages

All you gotta do is: follow the norm using basic logging. No need to use logmuse. Just type:

FOr example, something like:

```
_LOGGER = logging.getLogger(__name__)
```

At the top of each module, and then use `_LOGGER.debug` or whatever in the module. Now, to attach these to a CLI, all you gotta do is: 


## 1 Initialize

Just add to the `__init__.py` file:

```
import logmuse

logmuse.init_logger(PACKAGE)
```

Where `PACKAGE` is the name of your package. Now it will be set up with default parameters for your within-python-use.

**Do not add this code to client packages that do not implement CLIs. This is only for the CLI package**.


## 2 Add CLI args

When you build your argparser, add the logmuse CLI options with this:


```
parser = logmuse.add_logging_options(parser)
```

This will give you:

- `--verbosity`
- `--silent`
- `--logdev`

And your logger will automatically respond to these command-line arguments. (PS, pypiper already adds these; so if you're using pypiper add args, don't repeat)


## 3 Activate logmuse

At the top of your module file, say:

```
import logmuse
```

In your `main` function say:

```
global _LOGGER
_LOGGER = logmuse.logger_via_cli(args, make_root=True)
```

Here, `args` is the result of argparse.parse_args().

# How to link logmuse loggers

Say you have one package that uses logmuse and you want to link a logger from
another package so that the CLI arguments can control the imported package.

Not much you gotta do. Just do the above. that's it. Make sure your package isn't making a root logger or something silly like that.

Since we're initiating a root logger here that has the CLI, and all the others should propogate, their messages should get handled according to the settings of the root logger.








Old way:
```
# Set the logging level.
if args.dbg:
    # Debug mode takes precedence and will listen for all messages.
    level = args.logging_level or logging.DEBUG
elif args.verbosity is not None:
    # Verbosity-framed specification trumps logging_level.
    level = _LEVEL_BY_VERBOSITY[args.verbosity]
else:
    # Normally, we're not in debug mode, and there's no verbosity.
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
