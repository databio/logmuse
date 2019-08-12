# Using logmuse interactively


To set logmuse to DEBUG while in an interactive session, use:

```
logmuse.init_logger(PACKAGE, "DEBUG", devmode=True)
```

For example, for package divvy, which uses logmuse, run this in your interactive session:

```
logmuse.init_logger("divvy", "DEBUG", devmode=True)
```

