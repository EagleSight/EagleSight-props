# ESMAP Specifications

ESMAP are the file format used to descript the maps

### 1 x `uint16`: _Width_

The number of columns the map has.

### 1 x `uint16`: _Depth_

The number of rows the map has.

### 1 x `int16`: _Top_

The heighest point on the map.

### 1 x `float32`: _Distance_

The distance between 2 points on the X or Z axis.

### _Width_ x _Depth_ x `int16`: _Points_

The height (Y axis) of each points of the map, going line by line (X axis) then row by row (Z axis).

Exemple:
```
  X Axis ------>
  
00, 01, 02, 03, 04, 05, 06, 07, 08,  |
09, 10, 11, 12, 13, 14, 15, 16, 17,  |
18, 19, 20, 21, 22, 23, 24, 25, 26,  | Z Axis
27, 28, 29, 30, 31, 32, 33, 34, 35,  |
36, 37, 38, 39, 40, 41, 42, 43, 44,  |
45, 46, 47, 48, 49, 50, 51, 52, 53,  V
54, 55, 56, 57, 58, 59, 60, 61, 62,  
63, 64, 65, 66, 67, 68, 69, 70, 71,
72, 73, 74, 75, 76, 77, 78, 79, 80,
81, 82, 83, 84, 85, 86, 87, 88, 89  
```

###  _Width_ x _Depth_ x 3 x `uint8` : _Vextex color_
Each points is assigned an RGB color. Each vertices located at the same location share the same color.

### 1 x `uint8`: (optional) _Plants species count_.
Number of plants species in this map

## For each in _Plants species count_

### 1 x `uint16`: _Plant ID_
ID of the plant

### 1 x `uint16`: _Instances count_
Number of instances of this plant

### _Instances count_ x 2 x `float32`: _Plant location_
The first `float32` is for the X and the second for the Z axis. 
The Y axis is determined by the points in the map.


