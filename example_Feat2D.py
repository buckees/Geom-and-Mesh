"""Examples."""

import os
import glob
for i in glob.glob("*.png"):
    os.remove(i)

from LngmrMod_Geom import RctMod2D, Domain2D, Rectangle
from LngmrMod_Mesh import Mesh2D

# build the geometry
Feat2d = RctMod2D(name='Feat2d', is_cyl=False)
#               (left, bottom), (width, height)
domain2d = Domain2D((0.0, 0.0),    (200.0e-9, 500.0e-9))
Feat2d.add_domain(domain2d)

# Add metal wall to all boundaries
# In Metal, vector potential A = 0
#                        (left, bottom), (right, top)
bott = Rectangle('SiO2_', (0.0e-9, 0.0e-9), (200.0e-9, 50.0e-9))
Feat2d.add_shape(bott)
main = Rectangle('Si_', (0.0e-9, 50.0e-9), (200.0e-9, 400.0e-9))
Feat2d.add_shape(main)
PR_left = Rectangle('PR_', (0.0e-9, 400.0e-9), (50.0e-9, 450.0e-9)) 
Feat2d.add_shape(PR_left)
PR_right = Rectangle('PR_', (150.0e-9, 400.0e-9), (200.0e-9, 450.0e-9))
Feat2d.add_shape(PR_right)

Feat2d.plot(figsize=(4, 4), ihoriz=1)
print(Feat2d)

# generate mesh to imported geometry
mesh2d = Mesh2D(import_geom=Feat2d)
mesh2d.gen_mesh(ngrid=(50, 125))
mesh2d.plot(figsize=(4, 4), ihoriz=1, s_size=1)
