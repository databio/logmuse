# Tutorial

You are producing a CLI package that will use logmuse. Logmuse will provide command-line options to control logging, such as `--verbosity` and `--silent`. Here's how to set it up.

## Imported packages

For any packages that are imported by your CLI package, all you have to do is follow the normal usage of the built-in `logging` module. **No need to use logmuse in imported packages**. Just type, for example, something like:

```
_LOGGER = logging.getLogger(__name__)
```

At the top of each module, and then use `_LOGGER.debug` or whatever in the module. That's it. The command line arguments passed via your CLI will control the imported packages as well. Make sure your package isn't making a root logger or something silly like that.


## Your CLI package

Now, to use logmuse in your CLI package, *including* all imported loggers, all you have to do is: 

## 1 Initialize

Just add to the `__init__.py` file:

```
import logmuse
logmuse.init_logger(PACKAGE)
```

Where `PACKAGE` is the name of your package. Now it will be set up with default parameters for your within-python-use. Remember, **this is only for the CLI package.** Do not add this code to client packages that do not implement CLIs.


## 2 Add CLI args

When you build your argparser, add the logmuse CLI options with this:


```
parser = logmuse.add_logging_options(parser)
```

This will give you:

- `--verbosity`
- `--silent`
- `--logdev`

And your logger will automatically respond to these command-line arguments. (PS, [pypiper](http://pypiper.databio.org) uses logmuse to add these; so if you're using pypiper to add args, don't repeat).


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




## Old way

No need to read further. This is how it *used to* work, before it was awesome.

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

We should move the logging level stuff into logmuse
