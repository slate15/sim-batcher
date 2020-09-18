^j::

SetTimer, WatchCursor, 20

WatchCursor:
CoordMode, Mouse, Screen
MouseGetPos, xpos, ypos
Tooltip, xpos: %xpos%`nypos: %ypos%
return

esc::exitapp