####################################################################################################
#
# 2013 Fabrice Salvaire Update from pyprocps version v0.4
#
####################################################################################################

####################################################################################################
#
# $ cat /proc/$$/stat
#   5379 (ipython) S 2254 5379 2254 34823 5379 4202496 5939 0 1 0 38 45 0 0 20 0 2 0 44371114 315699200 4931 18446744073709551615 4194304 4196428 140734273904912 140734273900592 207646221587 0 0 16781312 134217730 18446744073709551615 0 0 17 2 0 0 0 0 0
#
# $ cat /proc/$$/status
#   Name:   ipython
#   State:  S (sleeping)
#   Tgid:   5379
#   Pid:    5379
#   PPid:   2254
#   TracerPid:      0
#   Uid:    519     519     519     519
#   Gid:    501     501     501     501
#   Utrace: 0
#   FDSize: 256
#   Groups: 48 501 502 503 507 508 509 532 533 544 548 550 1014 1017 1018
#   VmPeak:   366836 kB
#   VmSize:   307392 kB
#   VmLck:         0 kB
#   VmHWM:     18708 kB
#   VmRSS:     18708 kB
#   VmData:    89072 kB
#   VmStk:       172 kB
#   VmExe:         4 kB
#   VmLib:      9824 kB
#   VmPTE:       376 kB
#   VmSwap:        0 kB
#   Threads:        2
#   SigQ:   0/46596
#   SigPnd: 0000000000000000
#   ShdPnd: 0000000000000000
#   SigBlk: 0000000000000000
#   SigIgn: 0000000001001000
#   SigCgt: 0000000188000002
#   CapInh: 0000000000000000
#   CapPrm: 0000000000000000
#   CapEff: 0000000000000000
#   CapBnd: ffffffffffffffff
#   Cpus_allowed:   ffff
#   Cpus_allowed_list:      0-15
#   Mems_allowed:   00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000001
#   Mems_allowed_list:      0
#   voluntary_ctxt_switches:        1629
#   nonvoluntary_ctxt_switches:     339
# 
# The fields are as follows:
# 
#   * Name: Command run by this process.
#   
#   * State: Current state of the process.  One of "R (running)", "S (sleeping)", "D (disk sleep)",
#     "T (stopped)", "T (tracing stop)", "Z (zombie)", or "X (dead)".
#   
#   * Tgid: Thread group ID (i.e., Process ID).
#   
#   * Pid: Thread ID (see gettid(2)).
#   
#   * TracerPid: PID of process tracing this process (0 if not being traced).
#   
#   * Uid, Gid: Real, effective, saved set, and file system UIDs (GIDs).
#   
#   * FDSize: Number of file descriptor slots currently allocated.
#   
#   * Groups: Supplementary group list.
#   
#   * VmPeak: Peak virtual memory size.
#   
#   * VmSize: Virtual memory size.
#   
#   * VmLck: Locked memory size.
#   
#   * VmHWM: Peak resident set size ("high water mark").
#   
#   * VmRSS: Resident set size.
#   
#   * VmData, VmStk, VmExe: Size of data, stack, and text segments.
#   
#   * VmLib: Shared library code size.
#   
#   * VmPTE: Page table entries size (since Linux 2.6.10).
#   
#   * Threads: Number of threads in process containing this thread.
#   
#   * SigPnd, ShdPnd: Number of signals pending for thread and for process as a whole (see pthreads(7) and signal(7)).
#   
#   * SigBlk, SigIgn, SigCgt: Masks indicating signals being blocked, ignored, and caught (see signal(7)).
#   
#   * CapInh, CapPrm, CapEff: Masks of capabilities enabled in inheritable, permitted, and effective sets (see capabilities(7)).
#   
#   * CapBnd: Capability Bounding set (since kernel 2.6.26, see capabilities(7)).
#   
#   * Cpus_allowed: Mask of CPUs on which this process may run (since Linux 2.6.24, see cpuset(7)).
#   
#   * Cpus_allowed_list: Same as previous, but in "list format" (since Linux 2.6.26, see cpuset(7)).
#   
#   * Mems_allowed: Mask of memory nodes allowed to this process (since Linux 2.6.24, see cpuset(7)).
#   
#   * Mems_allowed_list: Same as previous, but in "list format" (since Linux 2.6.26, see cpuset(7)).
#   
#   * voluntary_context_switches, nonvoluntary_context_switches: Number of voluntary and involuntary context switches (since Linux 2.6.23).
#
####################################################################################################

"""Procps infomation. 

Eli Criffield <pyprocps@criffield.net>
http://eli.criffield.net/pyprocps
Dec 2005

This module parses the infomation in /proc on linux systems and presents it.

The pidinfo class does most everything you could want. 
Create an object with it and give it the pid of the process you want info 
about then object.attribute is whatever infomationa about the object you 
could want. for example;

import os 
import pyprocps
myinfo = pyprocps.pidinfo(os.getpid())
myinfo.rss # rss size
myinfo.ppid # parent pid

and so on for a compleate list of attributes see the docstring for the 
pidinfo class. Note: all info is real time myinfo.rss maybe diffrent a few 
seconds later.


Other functions include:
updatedb(filename) will make a database of "usefull" infomation about 
    every running process
    if you run it again on the same file it will just 
    add new infomation but will not delete infomation about 
    process that have died
    "usefull" is defined by the list USEFULLIST and is 
    described in the docstring for allusefull
scandb(filename)   reads the file created with updatedb and presents it as a 
    "usefull" list
allusefull()       a list of usefulllists of every process
boottime()         unix long time of last boot
uptimej()                  uptime in jiffies
uptime()           iptime in seconds
num_cpus()         how many cpus do we have
vmstat()           a list of vm info
meminfo()          a list of meminfo
hz_hack()          how many jiffies in a second
do_time()          formats seconds kinda like ps does


"""
try:
    import errno
    import posix
    import string
    import time
    import os
    import sys
except ImportError, e:
    raise ImportError (str(e) + """
A critical module was not found. Probably this operating system 
does not support it. pyprocps is intended for UNIX-like operating systems.""")

__version__ = '0.01'
__revision__ = '$Revision: 0.000 $'
__all__ = ['','']

STATLIST = [ 
    "pid",        # 0  The process ID.
    "comm",       # 1  The  filename of the executable, in parentheses
    "state",      # 2  One character from the string "RSDZTW"
    "ppid",       # 3  The PID of the parent
    "pgrp",       # 4  The process group ID of the process.
    "session",    # 5  The session ID of the process
    "tty_nr",     # 6  The tty the process uses
    "tpgid",      # 7  The  process group ID of the process which currently owns
        #    the tty that the process is connected to.
    "flags",      # 8  The kernel flags word of the process. see <linux/sched.h>.
    "minflt",     # 9  The number of minor faults the  process  has  made  which
        #    have not required loading a memory page from disk.
    "cminflt",    # 10 The  number of minor faults that the process's waited-for
        #    children have made.
    "majflt",     # 11 The number of major faults the  process  has  made  which
        #    have required loading a memory page from disk.
    "cmajflt",    # 12 The  number of major faults that the process's waited-for
        #    children have made.
    "utime",      # 13 The number of jiffies that this process has  been
        #    scheduled in user mode.
    "stime",      # 14 The  number  of jiffies that this process has been 
        #    scheduled in kernel mode
    "cutime",     # 15 The number of  jiffies  that  this  process's  waited-for
        #    children  have  been  scheduled  in  user mode
    "cstime",     # 16 The number of  jiffies  that  this  process's  waited-for
        #    children have been scheduled in kernel mode.
    "priority",   # 17 The  standard  nice  value,  plus  fifteen.  The value is
        #    never negative in the kernel.
    "nice",       # 18 The nice value ranges from 19 (nicest) to -19  (not  nice
        #    to others).
    "0",          # 19 This  value  is  hard  coded  to 0 as a placeholder for a
        #    removed field.
    "itrealvalue",# 20 The time in jiffies before the next SIGALRM  is  sent  to
        #    the process due to an interval timer.
    "starttime",  # 21 The  time  in  jiffies  the  process started after system
        #    boot.
    "vsize",      # 22 Virtual memory size in bytes.
    "rss",        # 23 Resident Set Size: number of pages  the  process  has  in
        #    real memory, minus 3 for administrative purposes. This is
        #    just the pages which count towards text, data,  or  stack
        #    space.   This  does not include pages which have not been
        #    demand-loaded in, or which are swapped out.
    "rlim",       # 24 Current limit in bytes on the rss of the process (usually
        #    4294967295 on i386).
    "startcode",  # 25 The address above which program text can run.
    "endcode",    # 26 The address below which program text can run.
    "startstack", # 27 The address of the start of the stack.
    "kstkesp",    # 28 The current value of esp (stack pointer), as found in the
        #    kernel stack page for the process.
    "kstkeip",    # 29 The current EIP (instruction pointer).
    "signal",     # 30 The bitmap of pending signals.
    "blocked",    # 31 The bitmap of blocked signals.
    "sigignore",  # 32 The bitmap of ignored signals.
    "sigcatch",   # 33 The bitmap of caught signals.
    "wchan",      # 34 This is the "channel" in which the  process  is  waiting.
    "nswap",      # 35 Number of pages swapped (not maintained).
    "cnswap",     # 36 Cumulative nswap for child processes (not maintained).
    "exit_signal",# 37 Signal to be sent to parent when we die.
    "processor",  # 38 CPU number last executed on
    "rt_priority",# 39 Real-time scheduling  priority, NULL if kernel < 2.5.19
    "policy",     # 40 Scheduling policy, NULL if kernel < 2.5.19
    "delayacct_blkio_ticks", # 41 Aggregated block I/O delays, measured in clock ticks (centiseconds).
    "guest_time",            # 42 Guest time of the process (time spent running a virtual CPU for a
                             # guest operating system), measured in clock  ticks  (divide by sysconf(_SC_CLK_TCK).
    "cguest_time"            # 43 Guest time of the process's children, measured in clock ticks (divide by sysconf(_SC_CLK_TCK).
]

STATUSLIST = [
    "Name",      # 0 Name
    "State",     # 1 State
    "Tgid",      # 2 Tgid
    "Pid",       # 3 Pid
    "PPid",      # 4 PPid
    "TracerPid", # 5 TracerPid
    "Uid",       # 6 Uid (4 element list)
    "Gid",       # 7 Gid (4 element list)
    "Utrace",    # 8
    "FDSize",    # 9 FDSize
    "Groups",    # 10 Groups (list)
    "VmPeak",    # 11 
    "VmSize",    # 12 VmSize
    "VmLck",     # 13 VmLck
    "VmHWM",     # 14
    "VmRSS",     # 15 VmRSS
    "VmData",    # 16 VmData
    "VmStk",     # 17 VmStk
    "VmExe",     # 18 VmExe
    "VmLib",     # 19 VmLib
    "VmPTE",     # 10 VmPTE
    "VmSwap",    # 21
    "Threads",   # 22 Threads
    "SigQ",      # 23 SigQ
    "SigPnd",    # 24 SigPnd
    "ShdPnd",    # 25 ShdPnd
    "SigBlk",    # 26 SigBlk
    "SigIgn",    # 27 SigIgn
    "SigCgt",    # 28 SigCgt
    "CapInh",    # 29 CapInh
    "CapPrm",    # 20 CapPrm
    "CapEff",    # 31 CapEff
    "CapBnd",    # 32 Capability Bounding set (since kernel 2.6.26, see capabilities(7)).
    "Cpus_allowed", # 33 Mask of CPUs on which this process may run (since Linux 2.6.24, see cpuset(7)).
    "Cpus_allowed_list", # 34 Same as previous, but in "list format" (since Linux 2.6.26, see cpuset(7)).
    "Mems_allowed", # 35 Mask of memory nodes allowed to this process (since Linux 2.6.24, see cpuset(7)).
    "Mems_allowed_list", # 36 Same as previous, but in "list format" (since Linux 2.6.26, see cpuset(7)).
    "voluntary_context_switches", # 37 nonvoluntary_context_switches: Number of voluntary and involuntary context switches (since Linux 2.6.23).
    "nonvoluntary_ctxt_switches" # 38
]


USEFULLIST = [ 
    "pid",        # 0  The process ID.
    "comm",       # 1  The  filename of the executable, in parentheses
    "state",      # 2  One character from the string "RSDZTW"
    "ppid",       # 3  The PID of the parent
    "pgrp",       # 4  The process group ID of the process.
    "session",    # 5  The session ID of the process
    "tty_nr",     # 6  The tty the process uses
    "tpgid",      # 7  The  process group ID of the process which currently owns
        #    the tty that the process is connected to.
    "flags",      # 8  The kernel flags word of the process. see <linux/sched.h>.
    "minflt",     # 9  The number of minor faults the  process  has  made  which
        #    have not required loading a memory page from disk.
    "cminflt",    # 10 The  number of minor faults that the process's waited-for
        #    children have made.
    "majflt",     # 11 The number of major faults the  process  has  made  which
        #    have required loading a memory page from disk.
    "cmajflt",    # 12 The  number of major faults that the process's waited-for
        #    children have made.
    "utime",      # 13 The number of jiffies that this process has  been
        #    scheduled in user mode.
    "stime",      # 14 The  number  of jiffies that this process has been 
        #    scheduled in kernel mode
    "cutime",     # 15 The number of  jiffies  that  this  process's  waited-for
        #    children  have  been  scheduled  in  user mode
    "cstime",     # 16 The number of  jiffies  that  this  process's  waited-for
        #    children have been scheduled in kernel mode.
    "priority",   # 17 The  standard  nice  value,  plus  fifteen.  The value is
        #    never negative in the kernel.
    "nice",       # 18 The nice value ranges from 19 (nicest) to -19  (not  nice
        #    to others).
    "0",          # 19 This  value  is  hard  coded  to 0 as a placeholder for a
        #    removed field.
    "itrealvalue",# 20 The time in jiffies before the next SIGALRM  is  sent  to
        #    the process due to an interval timer.
    "starttime",  # 21 The  time  in  jiffies  the  process started after system
        #    boot.
    "vsize",      # 22 Virtual memory size in bytes.
    "rss",        # 23 Resident Set Size: number of pages  the  process  has  in
        #    real memory, minus 3 for administrative purposes. This is
        #    just the pages which count towards text, data,  or  stack
        #    space.   This  does not include pages which have not been
        #    demand-loaded in, or which are swapped out.
    "rlim",       # 24 Current limit in bytes on the rss of the process (usually
        #    4294967295 on i386).
    "startcode",  # 25 The address above which program text can run.
    "endcode",    # 26 The address below which program text can run.
    "startstack", # 27 The address of the start of the stack.
    "kstkesp",    # 28 The current value of esp (stack pointer), as found in the
        #    kernel stack page for the process.
    "kstkeip",    # 29 The current EIP (instruction pointer).
    "signal",     # 30 The bitmap of pending signals.
    "blocked",    # 31 The bitmap of blocked signals.
    "sigignore",  # 32 The bitmap of ignored signals.
    "sigcatch",   # 33 The bitmap of caught signals.
    "wchan",      # 34 This is the "channel" in which the  process  is  waiting.
    "nswap",      # 35 Number of pages swapped (not maintained).
    "cnswap",     # 36 Cumulative nswap for child processes (not maintained).
    "exit_signal",# 37 Signal to be sent to parent when we die.
    "processor",  # 38 CPU number last executed on
    "rt_priority",# 39 Real-time scheduling  priority, NULL if kernel < 2.5.19
    "policy",     # 40 Scheduling policy, NULL if kernel < 2.5.19
    "size",       # 41 total program size
    "resident",   # 42 resident set size
    "share",      # 43 shared pages
    "text",       # 44 text (code)
    "lib",        # 45 library
    "data",       # 46 data/stack
    "dt",         # 47 dirty pages (unused in Linux 2.6)
    "wchan",      # 48 This is the "channel" in which the  process  is  waiting.
    "lastseen",   # 49 the unix lohg time this process was last seen
    "cmdline"     # 50 complete command line for the process, unless the
        #    whole  process  has been swapped out or the process is 
        #    a zombie. then its one null char
]

STATMLIST = [
    "size",       # 0 total program size
    "resident",   # 1 resident set size
    "share",      # 2 shared pages
    "text",       # 3 text (code)
    "lib",        # 4 library
    "data",       # 5 data/stack
    "dt"          # 6 dirty pages (unused in Linux 2.6) and thus -1
]

def alluseful(minage=0):
    """returns an list of lists of "useful" info as defined by the list 
    USEFULLIST if you wanted to know what channel all process where in 
    you could make an list = pyprocps.alluseful() then loop though and 
    see what element 48 is (48 because USEFULLIST[48] is wchan)
    this is the function used by updatedb to get all new info.
    the only command line arg is option and is the number of seconds old 
    a process must be to be included, thus giving it a 5 would skip the process
    that is gathering the info and anything else less then 5 seconds old

    for process_info in pyprocps.alluseful(): #get "useful" about every processes
        print process_info[1]  # print the file name of the executable 
            # USEFULLIST[1]   
    a USEFULLIST is as follows:

    USEFULLIST = [ 
        "pid",        # 0  The process ID.
        "comm",       # 1  The  filename of the executable, in parentheses
        "state",      # 2  One character from the string "RSDZTW"
        "ppid",       # 3  The PID of the parent
        "pgrp",       # 4  The process group ID of the process.
        "session",    # 5  The session ID of the process
        "tty_nr",     # 6  The tty the process uses
        "tpgid",      # 7  The  process group ID of the process which currently owns
            #    the tty that the process is connected to.
        "flags",      # 8  The kernel flags word of the process. see <linux/sched.h>.
        "minflt",     # 9  The number of minor faults the  process  has  made  which
            #    have not required loading a memory page from disk.
        "cminflt",    # 10 The  number of minor faults that the process's waited-for
            #    children have made.
        "majflt",     # 11 The number of major faults the  process  has  made  which
            #    have required loading a memory page from disk.
        "cmajflt",    # 12 The  number of major faults that the process's waited-for
            #    children have made.
        "utime",      # 13 The number of jiffies that this process has  been
            #    scheduled in user mode.
        "stime",      # 14 The  number  of jiffies that this process has been 
            #    scheduled in kernel mode
        "cutime",     # 15 The number of  jiffies  that  this  process's  waited-for
            #    children  have  been  scheduled  in  user mode
        "cstime",     # 16 The number of  jiffies  that  this  process's  waited-for
            #    children have been scheduled in kernel mode.
        "priority",   # 17 The  standard  nice  value,  plus  fifteen.  The value is
            #    never negative in the kernel.
        "nice",       # 18 The nice value ranges from 19 (nicest) to -19  (not  nice
            #    to others).
        "0",          # 19 This  value  is  hard  coded  to 0 as a placeholder for a
            #    removed field.
        "itrealvalue",# 20 The time in jiffies before the next SIGALRM  is  sent  to
            #    the process due to an interval timer.
        "starttime",  # 21 The  time  in  jiffies  the  process started after system
            #    boot.
        "vsize",      # 22 Virtual memory size in bytes.
        "rss",        # 23 Resident Set Size: number of pages  the  process  has  in
            #    real memory, minus 3 for administrative purposes. This is
            #    just the pages which count towards text, data,  or  stack
            #    space.   This  does not include pages which have not been
            #    demand-loaded in, or which are swapped out.
        "rlim",       # 24 Current limit in bytes on the rss of the process (usually
            #    4294967295 on i386).
        "startcode",  # 25 The address above which program text can run.
        "endcode",    # 26 The address below which program text can run.
        "startstack", # 27 The address of the start of the stack.
        "kstkesp",    # 28 The current value of esp (stack pointer), as found in the
            #    kernel stack page for the process.
        "kstkeip",    # 29 The current EIP (instruction pointer).
        "signal",     # 30 The bitmap of pending signals.
        "blocked",    # 31 The bitmap of blocked signals.
        "sigignore",  # 32 The bitmap of ignored signals.
        "sigcatch",   # 33 The bitmap of caught signals.
        "wchan",      # 34 This is the "channel" in which the  process  is  waiting.
        "nswap",      # 35 Number of pages swapped (not maintained).
        "cnswap",     # 36 Cumulative nswap for child processes (not maintained).
        "exit_signal",# 37 Signal to be sent to parent when we die.
        "processor",  # 38 CPU number last executed on
        "rt_priority",# 39 Real-time scheduling  priority, NULL if kernel < 2.5.19
        "policy",     # 40 Scheduling policy, NULL if kernel < 2.5.19
        "size",       # 41 total program size
        "resident",   # 42 resident set size
        "share",      # 43 shared pages
        "text",       # 44 text (code)
        "lib",        # 45 library
        "data",       # 46 data/stack
        "dt",         # 47 dirty pages (unused in Linux 2.6)
        "wchan",      # 48 This is the "channel" in which the  process  is  waiting.
        "lastseen",   # 49 the unix lohg time this process was last seen
        "cmdline"     # 50 complete command line for the process, unless the
            #    whole  process  has been swapped out or the process is 
            #    a zombie. then its one null char
    ]

    """
    allpidi=[]
    hz=hz_hack()
    uptimesec=uptime()
    pidc = pidinfo(1)
    for pid in posix.listdir('/proc'):
        if pid.isdigit():
            pidc.changepid(pid)
            pidi = pidc.useful
            if (uptimesec-(float(pidi[21])/hz)) > minage:
                allpidi.append(pidi)
    return allpidi


def updatedb(procdb,minage=0): 
    """Makes a snapshot of "useful" information about process at a given time
    and stores it in the file "procdb" as giving by the first arg
    The second arg is optional and is the number of seconds old
    a process must be to be included, thus giving it a 5 would skip the process
    that is gathering the info and anything else less then 5 seconds old
    this "procdb" can be read with scandb() and will return a list of list that
    follow the "USEFULLIST" format
    pyprocps.updatedb("/tmp/procdb") #saves process info to /tmp/procdb
    pyprocps.scandb("/tmp/procdb")[0][18] # shows the nice value (USEFULLIST[18]
    is "nice") saved about the first process

    running  pyprocps.updatedb("/tmp/procdb") again will update the db with
    current info but saving all info for processes that died.

    see the docstring of pyprocps.alluseful() for what a USEFULLIST contains

    """
    if os.path.isfile(procdb):
        newpsi = alluseful(minage)
        oldpsi = scandb(procdb)
        for ops in oldpsi:
            for nps in newpsi:
                # compair pid and start time
                if ops[0] == nps[0] and ops[21] == nps[21]:
                    # newer info exsists 
                    oldpsi = delpid(ops[0],oldpsi)
        for ops in oldpsi:
            newpsi.append(ops)
    else:
        newpsi = alluseful(minage)

    dbfd = open(procdb,'w')
    for line in newpsi:
        dbfd.write("%s\n"%" ".join(line))
    dbfd.close()

def delpid(pid,list):
    """only used nternally inside updatedb()
    """
    newlist = []
    for line in list:
        if line[0] != str(pid): 
            newlist.append(line)
    return newlist

def scandb(procdb):
    """returns an list of lists of "useful" info as defined by the list 
    USEFULLIST 
    This info is read in by file "procdb" that was created with updatedb()
    if you wanted to know what channel all process where in when the db
    was created  
    you could make an list = pyprocps.scandb("/tmp/procdb") then loop though and 
    see what element 48 is (48 because USEFULLIST[48] is wchan)
    this is the function used by updatedb to get all new info.

    pyprocps.updatedb("/tmp/procdb") # create db
    #get "useful" about every processes at the time /tmp/procdb was created
    for process_info in pyprocps.scandb("/tmp/procdb"): 
        print process_info[1]  # print the file name of the executable 
            # USEFULLIST[1]   


    see the docstring of pyprocps.alluseful() for what a USEFULLIST contains
    """
    if not os.path.isfile(procdb): 
        print '%s not a file'%procdb
        return "-1"
    dbfd = open(procdb,'r')
    ln = []
    for line in dbfd:
        ln.append(line.split())
    dbfd.close()
    return ln

def boottime():
    """ return unix logtime of last boot
    """
    upfd = open('/proc/stat','r')
    for line in upfd:
        split = line.split()
        if split[0] == "btime":
            boottime = split[1]
    upfd.close()
    return boottime

def stat():
    """ return stat info
    """
    out = {}
    upfd = open('/proc/stat','r')
    for line in upfd:
        split = line.split()
        if split[0].startswith('cpu') :
            out[split[0]] = {}
            out[split[0]]["UMODE"] =  split[1]
            out[split[0]]["UMODELOW"] =  split[2]
            out[split[0]]["SYSMODE"] =  split[3]
            out[split[0]]["IDLE"] =  split[4]
        else:
            out[split[0]] = split[1]
    upfd.close()
    return out

def uptimej():
    """ return the uptime in jiffies
    """
    buf = open('/proc/stat','r')
    jarr = buf.read().split()
    buf.close()
    return float(jarr[1]) + float(jarr[2]) + float(jarr[3]) + float(jarr[4])


def uptime():
    """ return the uptime in seconds
    """
    upfd = open('/proc/uptime','r')
    upfs = float(upfd.read().split()[0])
    upfd.close()
    return upfs

def num_cpus():
    """ return the number of cpus
    """
    buf = open('/proc/stat','r')
    cpus = -1
    for line in buf:
        cpus = cpus + line.count('cpu')
    return cpus

def vmstat():
    """ return a dictionary of infomation about virtal memory as found in 
    /proc/vmstat, with the following keys:
    nr_dirty
    nr_writeback
    nr_unstable
    nr_page_table_pages
    nr_mapped
    nr_slab
    pgpgin
    pgpgout
    pswpin
    pswpout
    pgalloc_high
    pgalloc_normal
    pgalloc_dma
    pgfree
    pgactivate
    pgdeactivate
    pgfault
    pgmajfault
    pgrefill_high
    pgrefill_normal
    pgrefill_dma
    pgsteal_high
    pgsteal_normal
    pgsteal_dma
    pgscan_kswapd_high
    pgscan_kswapd_normal
    pgscan_kswapd_dma
    pgscan_direct_high
    pgscan_direct_normal
    pgscan_direct_dma
    pginodesteal
    slabs_scanned
    kswapd_steal
    kswapd_inodesteal
    pageoutrun
    allocstall
    pgrotated
    nr_bounce
    """
    fp = open('/proc/vmstat', 'r')
    rn = {}
    for line in fp:
        split = line.split()
        rn[split[0]] = split[1]
    fp.close()
    return rn

def meminfo():
    """ return a dictionary of memory infomation as found in /proc/meminfo
    this is some of the same infomation found in the linux command free
    the keys are as follows:
    MemTotal:
    MemFree:
    Buffers:
    Cached:
    SwapCached:
    Active:
    Inactive:
    HighTotal:
    HighFree:
    LowTotal:
    LowFree:
    SwapTotal:
    SwapFree:
    Dirty:
    Writeback:
    Mapped:
    Slab:
    CommitLimit:
    Committed_AS:
    PageTables:
    VmallocTotal:
    VmallocUsed:
    VmallocChunk:
    HugePages_Total:
    HugePages_Free:
    Hugepagesize:
    """
    fp = open('/proc/meminfo', 'r')
    rn = {}
    for line in fp:
        split = line.split()
        rn[split[0].replace(':','')] = split[1]
    fp.close()
    return rn

def hz_hack():
    """
    # from pyprocps src
    ######################################################################
    # Some values in /proc are expressed in units of 1/HZ seconds, where HZ
    # is the kernel clock tick rate. One of these units is called a jiffy.
    # The HZ value used in the kernel may vary according to hacker desire.
    # According to Linus Torvalds, this is not true. He considers the values
    # in /proc as being in architecture-dependant units that have no relation
    # to the kernel clock tick rate. Examination of the kernel source code
    # reveals that opinion as wishful thinking.
    #
    # In any case, we need the HZ constant as used in /proc. (the real HZ value
    # may differ, but we don't care) There are several ways we could get HZ:
    #
    # 1. Include the kernel header file. If it changes, recompile this library.
    # 2. Use the sysconf() function. When HZ changes, recompile the C library!
    # 3. Ask the kernel. This is obviously correct...
    #
    # Linus Torvalds won't let us ask the kernel, because he thinks we should
    # not know the HZ value. Oh well, we don't have to listen to him.
    # Someone smuggled out the HZ value. :-)
    #
    # This code should work fine, even if Linus fixes the kernel to match his
    # stated behavior. The code only fails in case of a partial conversion.
    #
    # Recent update: on some architectures, the 2.4 kernel provides an
    # ELF note to indicate HZ. This may be for ARM or user-mode Linux
    # support. This ought to be investigated. Note that sysconf() is still
    # unreliable, because it doesn't return an error code when it is
    # used with a kernel that doesn't support the ELF note. On some other
    # architectures there may be a system call or sysctl() that will work.
    ######################################################################
    """
    while 1:
        up1fd = open('/proc/uptime','r')
        up_1r = up1fd.read()
        buf = open('/proc/stat','r')
        jarrr = buf.readline()
        up2fd = open('/proc/uptime','r')
        up_2r = up2fd.read()
        buf.close()
        up1fd.close()
        up2fd.close()
        up_1 = float(up_1r.split()[0])
        up_2 = float(up_2r.split()[0])
        jarr = jarrr.split()
        jiffies =  float(jarr[1]) + float(jarr[2]) + float(jarr[3]) + float(jarr[4])
        if not ( (up_2-up_1)*1000/up_1 ): break
    seconds = (up_1 + up_2 )/ 2
    h = (jiffies/seconds/num_cpus())
    if h > 9 and h < 11:      return 10   # S/390 (sometimes) 
    if h > 18 and h < 22:     return 20   # user-mode Linux 
    if h > 30 and h < 34:     return 34   # ia64 emulator
    if h > 48 and h < 52:     return 50  
    if h > 58 and h < 61:     return 60
    if h > 62 and h < 65:     return 64   # StrongARM /Shark
    #if h > 95 and h < 105:    return 100  # normal Linux
    if h > 90 and h < 110:    return 100  # normal Linux
    if h > 124 and h < 132:   return 128  # MIPS, ARM 
    if h > 195 and h < 204:   return 200  # normal << 1
    if h > 253 and h < 260:   return 256
    if h > 393 and h < 408:   return 400  # normal << 2 
    if h > 790 and h < 808:   return 800  # normal << 3 
    if h > 990 and h < 1010:  return 1000 # ARM
    if h > 1015 and h < 1035: return 1024 # Alpha, ia64 
    if h > 1180 and h < 1220: return 1200 # Alpha
    #print "HZ %s UNKNOWN guessing 100?"%h
    return 100

def do_time(t):
    """ try to format time giving in seconds to look nice, like the output
    of ps
    """
    ss = t%60
    t = t/60
    mm = t%60 
    t = t/60
    hh = t%24
    t = t/24
    if t >= 1:
        return "%d-%02d:%02d:%02d"%(t,hh,mm,ss)
    if hh >= 10:
        return "%02d:%02d:%02d"%(hh,mm,ss)
    if hh >= 1:
        return "%01d:%02d:%02d"%(hh,mm,ss)
    if mm >= 10:
        return "%02d:%02d"%(mm,ss)
    return "%01d:%02d"%(mm,ss)


class pidinfo(object):
    """ Create an object who's attributes are infomation about the pid
    example: 
    init_info = pyprocps.pidinfo("1")
    init_info.state # is the state of pid 1 (init)
    possible attributes are:

    pid:           The process ID.
    comm:          The  filename of the executable: in parentheses
    state:         One character from the string RSDZTW
    ppid:          The PID of the parent
    pgrp:          The process group ID of the process.
    session:       The session ID of the process
    tty_nr:        The tty the process uses
    tpgid:         The  process group ID of the process which currently owns
        the tty that the process is connected to.
    flags:         The kernel flags word of the process. see <linux/sched.h>.
    minflt:        The number of minor faults the  process  has  made  which
        have not required loading a memory page from disk.
    cminflt:      The  number of minor faults that the process's waited-for
        children have made.
    majflt:       The number of major faults the  process  has  made  which
        have required loading a memory page from disk.
    cmajflt:      The  number of major faults that the process's waited-for
        children have made.
    utime:        The number of jiffies that this process has  been
        scheduled in user mode.
    stime:        The  number  of jiffies that this process has been
        scheduled in kernel mode
    cutime:       The number of  jiffies  that  this  process's  waited-for
        children  have  been  scheduled  in  user mode
    cstime:       The number of  jiffies  that  this  process's  waited-for
        children have been scheduled in kernel mode.
    priority:     The  standard  nice  value:  plus  fifteen.  The value is
        never negative in the kernel.
    nice:         The nice value ranges from 19 (nicest) to -19  (not  nice
        to others).
    0:            This  value  is  hard  coded  to 0 as a placeholder for a
        removed field.
    itrealvalue:  The time in jiffies before the next SIGALRM  is  sent  to
        the process due to an interval timer.
    starttime:    The  time  in  jiffies  the  process started after system
        boot.
    vsize:        Virtual memory size in bytes.
    rss:          Resident Set Size: number of pages  the  process  has  in
        real memory: minus 3 for administrative purposes. This is
        just the pages which count towards text: data:  or  stack
        space.   This  does not include pages which have not been
        demand-loaded in: or which are swapped out.
    rlim:         Current limit in bytes on the rss of the process (usually
        4294967295 on i386).
    startcode:    The address above which program text can run.
    endcode:      The address below which program text can run.
    startstack:   The address of the start of the stack.
    kstkesp:      The current value of esp (stack pointer): as found in the
        kernel stack page for the process.
    kstkeip:      The current EIP (instruction pointer).
    signal:       The bitmap of pending signals.
    blocked:      The bitmap of blocked signals.
    sigignore:    The bitmap of ignored signals.
    sigcatch:     The bitmap of caught signals.
    wchan:        This is the channel in which the  process  is  waiting.
    nswap:        Number of pages swapped (not maintained).
    cnswap:       Cumulative nswap for child processes (not maintained).
    exit_signal:  Signal to be sent to parent when we die.
    processor:    CPU number last executed on
    rt_priority:  Real-time scheduling  priority: NULL if kernel < 2.5.19
    policy        Scheduling policy: NULL if kernel < 2.5.19
    size:         total program size
    resident:     resident set size
    share:        shared pages
    text:         text (code)
    lib:          library
    data:         data/stack
    dt:           dirty pages (unused in Linux 2.6) and thus -1
    Name:         Name
    State:        State
    SleepAVG:     SleepAVG
    Tgid:         Tgid
    Pid:          Pid
    PPid:         PPid
    TracerPid:    TracerPid
    Uid:          Uid (4 element list)
    Gid:          Gid (4 element list)
    FDSize:       FDSize
    Groups:       Groups (list)
    VmSize:       VmSize
    VmLck:        VmLck
    VmRSS:        VmRSS
    VmData:       VmData
    VmStk:        VmStk
    VmExe:        VmExe
    VmLib:        VmLib
    VmPTE:        VmPTE
    Threads:      Threads
    SigQ:         SigQ
    SigPnd:       SigPnd
    ShdPnd:       ShdPnd
    SigBlk:       SigBlk
    SigIgn:       SigIgn
    SigCgt:       SigCgt
    CapInh:       CapInh
    CapPrm:       CapPrm
    CapEff:       CapEff
    cwd:          The current working directory
    exe:          The path of the file that was executed for this process
    root:         The path to this processes root
    wchan:        the channel the process is in
    environ:      a dictionary of envorment varibales for this process
    loginuid:     the loginuid
    cmdline:      the cmdline (with nulls insted of spaces)
    formatedtime: the time formated to look like time from ps
    useful:      a list that includes everything in the USEFULLIST
        see the docstring for pyprocps.alluseful()for whats in a 
        USEFULLIST
    useful_dict: a dictionary of the above so process.useful_dict['cmdline']
        is the same as process.cmdline
"""

    def __init__(self,pid):
        self.__pid = pid 

    def __getattribute__(self,attr):
        try: return object.__getattribute__(self,attr)
        except AttributeError:
            if attr in STATLIST:
                return self.__get_stat_dict()[attr]
            if attr in STATMLIST:
                return self.__get_statm_dict()[attr]
            if attr in STATUSLIST :
                return self.__get_status()[str(attr)]
            if attr == 'cwd' :
                return self.__get_cwd()
            if attr == 'exe' :
                return self.__get_exe()
            if attr == 'root' :
                return self.__get_root()
            if attr == 'wchan' :
                return self.__get_wchan()
            if attr == 'environ' :
                return self.__get_environ()
            if attr == 'loginuid' :
                return self.__get_loginuid()
            if attr == 'cmdline' :
                return self.__get_cmdline()
            if attr == 'time' :
                return self.__get_time()
            if attr == 'formatedtime' :
                return self.__get_formated_time()
            if attr == 'useful' :
                return self.__get_useful()
            if attr == 'useful_dict' :
                return self.__get_useful_dict()
            raise AttributeError

    def changepid(self,pid):
        self.__pid = pid

    def __get_useful(self):
        useful = self.__get_stat()
        useful.extend(self.__get_statm())
        useful.append(self.__get_wchan())
        useful.append(str(time.time()))
        useful.append(self.__get_cmdline())
        return useful

    def __get_stat(self):
        # see man proc for /proc/pid/stat layout        
        fp = open('/proc/%s/stat' % (self.__pid,), 'r')
        ln = string.split(fp.read())
        # 2.5.19+ has 41 under 2.5.19 have 39
        while len(ln) < 41:
            ln.append("-1")
        fp.close()
        return ln

    def __get_statm(self):
        # see man proc for /proc/pid/statm layout       
        fp = open('/proc/%s/statm' % (self.__pid,), 'r')
        ln = string.split(fp.read())
        # 2.6 has 6 everything else has 7
        while len(ln) < 7:
            ln.append("-1")
        fp.close()
        return ln

    def __get_stat_dict(self):
        dict = {}
        cnt=0
        for line in self.__get_stat():
            dict[STATLIST[cnt]] = line
            cnt=cnt+1
        return dict

    def __get_statm_dict(self):
        dict = {}
        cnt=0
        for line in self.__get_statm():
            dict[STATMLIST[cnt]] = line
            cnt=cnt+1
        return dict

    def __get_useful_dict(self):
        dict = {}
        cnt=0
        for line in self.__get_useful():
            dict[USEFULLIST[cnt]] = line
            cnt=cnt+1
        return dict

    def __get_cwd(self):
        return os.readlink('/proc/%s/cwd' % (self.__pid,))

    def __get_exe(self):
        try:
            exe = os.readlink('/proc/%s/exe' % (self.__pid,))
        except OSError:
            exe = None
        return exe

    def __get_root(self):
        return os.readlink('/proc/%s/root' % (self.__pid,))

    def __get_wchan(self):
        # 2.4 has no wchan ? maybe no i86 has no wchan?
        try:
            fp = open('/proc/%s/wchan' % (self.__pid,), 'r')
        except IOError:
            return "-1"
        else :
            ln = fp.read()
            fp.close()
            return ln

    def __get_environ(self):
        fp = open('/proc/%s/environ' % (self.__pid,), 'r')
        rn = {}
        list = fp.read().split("\000")
        for line in list:
            split = line.split("=",1)
            if len(split) <= 1 : continue
            rn[split[0]] = split[1]
        fp.close()
        return rn

    def __get_loginuid(self):
        fp = open('/proc/%s/loginuid' % (self.__pid,), 'r')
        ln = fp.read()
        fp.close()
        return ln

    def __get_cmdline(self):
        # see man proc for /proc/pid/stat layout        
        fp = open('/proc/%s/cmdline' % (self.__pid,), 'r')
        cmdline = fp.readline()
        fp.close()
        if cmdline == '': cmdline = '\000' 
        return cmdline.replace(' ','\000')

    def __get_status(self):
        fp = open('/proc/%s/status'%self.__pid, 'r')
        rn = {}
        for line in fp:
            split = line.split()
            rn[split[0].replace(':','')] = split[1:]
        fp.close()
        return rn

    def __get_time(self):
        status = self.__get_stat()
        return (float(status[14]) + float(status[15]))/hz_hack()

    def __get_formated_time(self):
        return do_time(self.__get_time())

####################################################################################################
#
# End
#
####################################################################################################
