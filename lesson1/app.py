import numpy as np

lines = []
filename = 'triangle.obj'

# v: vertices vn: normals
lines.append('v 0 0 0')
lines.append('vn 0 0 -1')
lines.append('v 1 0 0')
lines.append('vn 0 0 -1')
lines.append('v 0 1 0')
lines.append('vn 0 0 -1')

# vt: uv coordinates
lines.append('vt 0 0')
lines.append('vt 1 0')
lines.append('vt 0 1')

# f: faces
lines.append('f 1 2 3')
# lines.append('f 1/1/1 2/2/2 3/3/3')

with open(filename, 'w') as f:
    for str in lines:
        f.write(str)
        f.write('\n')