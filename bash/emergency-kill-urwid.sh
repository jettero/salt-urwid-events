#!/bin/bash

function newk_urwid() {
    pgrep -f python.*urwid  | sudo xargs -trn1 kill -2
    pgrep -f python.*uevent | sudo xargs -trn1 kill -2
}
