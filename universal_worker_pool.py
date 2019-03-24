#!/usr/bin/python3
import subprocess
from os import path, makedirs, getcwd, chdir, devnull
import matplotlib.pyplot as plt
from multiprocessing import Pool, TimeoutError, cpu_count

class Job:
    def __init__(self, command=[], function=None, args=[], how_many_in_parallel=0, priority=1, timeout=None, checkFunc=None, checkArgs=[]):
        self.cmd_ = command
        self.func_ = function
        self.args_ = args
        self.checkFunc_ = checkFunc
        self.checkArgs_ = checkArgs
        self.priority_ = priority
        self.timeout_ = timeout
        if not how_many_in_parallel:
            self.nthreads = cpu_count()
        elif how_many_in_parallel == -1:
            self.nthreads = cpu_count() - 1
        else:
            self.nthreads = how_many_in_parallel

def execute_job(j):
    if j.checkFunc_ is not None:
        if j.checkFunc_(j.checkArgs_):
            print("["str(n_launched+n_skipped)+'/'+str(jobcount)+"]\tSkipping a finished job")
            n_skipped += 1
            return 0
    n_launched += 1
    if len(j.cmd_):
        print("["str(n_launched+n_skipped)+'/'+str(jobcount)+"]\t"+" ".join(j.cmd_))
        r = subprocess.call(j, timeout=j.timeout_, capture_output=False)
    else if j.func_ is not None:
        print("["str(n_launched+n_skipped)+'/'+str(jobcount)+"]\t"+j.func_.__name__+'('+", ".join(j.args_)+')')
        try:
            r = j.func_(j.args_)
        except:
            r = 1
            pass
    n_finished += 1
    return r

######################## HERE DEFINE YOUR JOBS ############################""#

joblist = []

# joblist.append( Job(command = ["command", "arg1", "arg2", ... ,"argN"]) )
# joblist.append( Job(function = functionName, args=[list, of, args]) )

#### To specify that tasks should be excuted before some others, use the priority arg:

# joblist.append( Job("commandline to execute first", priority=1) )
# joblist.append( Job("commandline to execute then", priority=2) )
# joblist.append( Job("commandline to execute at last", priority=...someNumber ) )

#### If a task already uses several cores and you wish to specify how many tasks of that type you allow
#### to run in parallel, use the how_many_in_parallel argument:
# joblist.append( Job(command = ["command", "arg1", "arg2", ... ,"argN"], how_many_in_parallel=1) )
#### Tip: set the argument to -1 to use all cores but one.

#### if you re-run an interrupted session, use functions to check if the computation needs to be redone:
# joblist.append( Job(command = ["command", "arg1", "arg2", ... ,"argN"], checkFunc=someFunction, checkArgs=[]) )
#### where someFunction(checkArgs) returns 1 if the computation has already been finished previously

#### to give up a job after some time, use the timeout argument in seconds:
# joblist.append( Job(command = ["command", "arg1", "arg2", ... ,"argN"], timeout=3600) )






###############################################################################

jobs = { 1:{}, 2:{} }
jobcount = len(joblist)
for job in joblist:
    if job.nthreads not in jobs[job.priority_].keys():
        jobs[job.priority_][job.nthreads] = []
    jobs[job.priority_][job.nthreads].append(job)
nprio = max(jobs.keys())


n_launched = 0
n_finished = 0
n_skipped = 0
for i in range(1,nprio+1):

    # check the thread numbers
    different_thread_numbers = [n for n in jobs[i].keys() ]
    different_thread_numbers.sort()

    for n in different_thread_numbers:
        bunch = jobs[i][n]
        pool = Pool(processes=n)
        results = [ x for x in pool.map(execute_job, bunch)]

