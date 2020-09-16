^j::

Tooltip, Relative
sleep, 1000

CoordMode, ToolTip, Relative
CoordMode, Pixel, Relative
CoordMode, Mouse, Relative
CoordMode, Caret, Relative
CoordMode, Menu, Relative

SetTimer, WatchCursor, 20

WatchCursor:
MouseGetPos, xpos, ypos
Tooltip, xpos: %xpos%`nypos: %ypos%
return

esc::exitapp