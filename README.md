# CommunistWorkers
A script to define a bunch of user-provided mono-threaded, pluri-threaded and multi-threaded jobs, and run them to completion.
Supports both command line tasks and python-function-runs (with args).

Supports priorities over the tasks in the bunch.

Supports checking if the task has been previously computed before launching it (useful in case of crash/re-run).

Supports giving up a task after some time out trying.

Coming soon: logging, colors

# How to use
Define jobs with your own python code in the appropriate part of the script.
Examples:

```
joblist.append( Job(command = ["command", "arg1", "arg2", ... ,"argN"]) )
joblist.append( Job(function = functionName, args=[list, of, args]) )
```

To specify that tasks should be excuted before some others, use the priority arg:

```
joblist.append( Job("commandline to execute first", priority=1) )
joblist.append( Job("commandline to execute then", priority=2) )
joblist.append( Job("commandline to execute at last", priority=...someNumber ) )
```

If a task already uses several cores and you wish to specify how many tasks of that type you allow to run in parallel, use the how_many_in_parallel argument:
```
joblist.append( Job(command = ["command", "arg1", "arg2", ... ,"argN"], how_many_in_parallel=1) )
```
Tip: set the argument to -1 to use all cores but one.

If you re-run an interrupted session, use functions to check if the computation needs to be redone:
```
joblist.append( Job(command = ["command", "arg1", "arg2", ... ,"argN"], checkFunc=someFunction, checkArgs=[]) )
```
where someFunction(checkArgs) returns 1 if the computation has already been finished previously

To give up a job after some time, use the timeout argument in seconds:
```
joblist.append( Job(command = ["command", "arg1", "arg2", ... ,"argN"], timeout=3600) )
```
