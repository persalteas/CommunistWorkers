# CommunistWorkers
A script to define a bunch of user-provided mono-threaded, pluri-threaded and multi-threaded jobs, and run them to completion.
Supports both command line tasks and python-function-runs (with args).
Supports priorities over the tasks in the bunch.
Supports checking if the task has been previously computed before launching it (useful in case of crash/re-run)
Coming soon: logging, colors
