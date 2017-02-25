#!/bin/bash

function newk_urwid() {
    for i in 2 15 9; do
        pgrep -f python.*urwid  | sudo xargs -trn1 kill -$i
        pgrep -f python.*uevent | sudo xargs -trn1 kill -$i
    done
}
