#!/usr/bin/env bash

# NOTE: While testing this app, it's sometimes necessary to kill the forked background proceses
#       They should suicide when the urwid portion of the app dies, but they sometimes do not.
#
#       Also, sometimes the cursor isn't restored at the end

my_dir="$(dirname "$0")"
u_py="$my_dir/uevents.py"
u_log="$my_dir/uevents.log"

source bash/emergency-kill-urwid.sh

rm -vf "$u_log"

"$u_py" "$@"

newk_urwid
echo -n $'\x1b'"[?25h"

[ -n "$LINES" ] || LINES=25
tx=$(( LINES - 2 ))
tail -n $tx "$u_log"
