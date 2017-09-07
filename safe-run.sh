#!/usr/bin/env bash

# NOTE: While testing this app, it's sometimes necessary to kill the forked background proceses
#       They should suicide when the urwid portion of the app dies, but they sometimes do not.
#
#       Also, sometimes the cursor isn't restored at the end

source limit-shell.sh

my_dir="$(dirname "$0")"
cd "$my_dir" || exit

source bash/emergency-kill-urwid.sh

rm -vf uevents.log

${USE_PYTHON} ./uevents.py "$@"

newk_urwid
echo -n $'\x1b'"[?25h"

[ -n "$LINES" ] || LINES=25
tx=$(( LINES - 2 ))
tail -n $tx uevents.log
