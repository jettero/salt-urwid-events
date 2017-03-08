#!/bin/bash

# It comes up surprisingly frequently that the forking backend goes insane and
# takes down my whole aws instance for a while (until the OOM gets to it).
# this helps to shut the beast down until I find whatever the next bug is.

function newk_urwid() {
    for i in 2 15 9; do
        pgrep -f python.*urwid  | sudo xargs -trn1 kill -$i
        pgrep -f python.*uevent | sudo xargs -trn1 kill -$i
    done
}
