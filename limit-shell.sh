#!/source/this/bash

set -x

ulimit -u 80 # simple minor bugs in the forking have crashed my dev host,
             # trigging ridiculous oom decisions
             # ∃ burried code within the application to set oom priority
             # to kill me first, but ulimit seems smart anyway

# I added these off the top of my head as resonably large numbers that will
# still leave the system salvagable after a fork-bomb accident (maybe)

ulimit -c 1000  # core file size          (blocks, -c) 0
ulimit -e 15    # scheduling priority             (-e) 0
ulimit -d 3000  # data seg size           (kbytes, -d) unlimited
ulimit -m 3000  # max memory size         (kbytes, -m) unlimited
ulimit -t 3600  # cpu time               (seconds, -t) unlimited
ulimit -v 5000  # virtual memory          (kbytes, -v) unlimited

set +x

# file size               (blocks, -f) unlimited
# pending signals                 (-i) 63562
# max locked memory       (kbytes, -l) 64
# open files                      (-n) 1024
# pipe size            (512 bytes, -p) 8
# POSIX message queues     (bytes, -q) 819200
# real-time priority              (-r) 0
# stack size              (kbytes, -s) 8192
# max user processes              (-u) 63562
# file locks                      (-x) unlimited

# Options:
#   -S        use the `soft' resource limit
#   -H        use the `hard' resource limit
#   -a        all current limits are reported
#   -b        the socket buffer size
#   -c        the maximum size of core files created
#   -d        the maximum size of a process's data segment
#   -e        the maximum scheduling priority (`nice')
#   -f        the maximum size of files written by the shell and its children
#   -i        the maximum number of pending signals
#   -l        the maximum size a process may lock into memory
#   -m        the maximum resident set size
#   -n        the maximum number of open file descriptors
#   -p        the pipe buffer size
#   -q        the maximum number of bytes in POSIX message queues
#   -r        the maximum real-time scheduling priority
#   -s        the maximum stack size
#   -t        the maximum amount of cpu time in seconds
#   -u        the maximum number of user processes
#   -v        the size of virtual memory
#   -x        the maximum number of file locks
#   -T    the maximum number of threads
