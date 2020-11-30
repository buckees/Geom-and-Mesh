"""Examples."""

import os
import glob
for i in glob.glob("*.png"):
    os.remove(i)

from LngmrMod_Geom import RctMod1D, Domain1D, Interval
from LngmrMod_Mesh import Mesh1D

"""Test 1D Geometry."""
ICP1d = RctMod1D(name='ICP1D', is_cyl=False)
domain1d = Domain1D(domain=(-10.0, 10.0))
ICP1d.add_domain(domain1d)
seg1 = Interval('M', (-10.0, -8.0))
ICP1d.add_shape(seg1)
seg2 = Interval('M', (5.0, 10.0))
ICP1d.add_shape(seg2)
seg3 = Interval('D', (-6.0, 0.0))
ICP1d.add_shape(seg3)
ICP1d.plot()
print(ICP1d)

# generate mesh to imported geometry
mesh1d = Mesh1D(import_geom=ICP1d)
mesh1d.gen_mesh(nx=100)
mesh1d.plot()