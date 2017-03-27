About
=====

This is my attempt to represent Salt events in a TUI.
There is much work to be done.

TODO
====

- the jobs view should do a better job of showing what's happening
  - what chagned on state runs?
  - which hosts returned (if there's room to show this)

- the detail view for a particular jid in the jobs view
  - should update as new items come in (currently the view is frozen at the
    point of click through)
  - if most of the events in the detail view have the same outputter,
    or possibly, if the publish has an outputter... we should be able to show
    the whole (eg) state-run using the intended outputter
