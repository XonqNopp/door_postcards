Door postcards 2.0
##################

This little script is here to get coordinates of where to put a postcard on the door.

The door measures 800x2000mm

The script allows to get coordinates in Cartesian (x,z) or polar (r,phi) coordinates.

The origin is the bottom left corner of the door.
Each postcard is referenced by its bottom left corner.
The typical size of a postcard is A6, which measures 146x106mm

All the occupied location are stored in the file busy.csv.

Based on this, the script gives the coordinates of a free random location.

Ideas for future:

* https://en.wikipedia.org/wiki/Coordinate_system#Other_commonly_used_systems
* https://www.johndcook.com/blog/2020/11/09/some-mathematical-art/
* esoteric coordinate systems
* map projections, saying the door is the northern hemisphere
* curve with computation of integral up to the point where it shall be pinned
