#!/usr/bin/env bash

# NOTE: While testing this app, it's sometimes necessary to kill the forked background proceses
#       They should suicide when the urwid portion of the app dies, but they sometimes do not.
#
#       Also, sometimes the cursor isn't restored at the end

ulimit -u 50 # simple minor bugs in the forking have crashed my dev host,
             # trigging ridiculous oom decisions
             # ∃ burried code within the application to set oom priority
             # to kill me first, but ulimit seems smart anyway

my_dir="$(dirname "$0")"
cd "$my_dir" || exit

source bash/emergency-kill-urwid.sh

rm -vf uevents.log

./uevents.py "$@"

newk_urwid
echo -n $'\x1b'"[?25h"

[ -n "$LINES" ] || LINES=25
tx=$(( LINES - 2 ))
tail -n $tx uevents.log
