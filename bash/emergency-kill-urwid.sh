#!/bin/bash

function newk_urwid() {
    pgrep -f python.*urwid | sudo xargs -trn1 kill -2
}
