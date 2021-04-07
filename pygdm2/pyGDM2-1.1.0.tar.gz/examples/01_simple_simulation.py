# encoding: utf-8
from pyGDM2 import structures
from pyGDM2 import materials
from pyGDM2 import propagators
from pyGDM2 import fields
from pyGDM2 import core
from pyGDM2 import visu

## --- alternatively use new API:
# from pyGDM2 import fields_py as fields
# from pyGDM2 import core_py as core

## --- simulation initialization ---
## structure: sphere of 160nm radius,
## constant dielectric function,
step = 20
geometry = structures.sphere(step, R=8.2, mesh='cube')
material = materials.dummy(2.0)
struct = structures.struct(step, geometry, material)

## incident field: plane wave, 400nm, lin. pol. along X
field_generator = fields.plane_wave
wavelengths = [400]
kwargs = dict(inc_angle=0, inc_plane='xz', theta=0)
efield = fields.efield(field_generator, 
               wavelengths=wavelengths, kwargs=kwargs)

## environment: vacuum
n1 = 1.0
dyads = propagators.DyadsQuasistatic123(n1)

## create simulation object
sim = core.simulation(struct, efield, dyads)


## --- run the simulation ---
core.scatter(sim, method='cupy')


## --- plot the near-field inside the sphere ---
## using first (of one) field-config (=index 0)
## slice through sphere center
visu.vectorfield_color_by_fieldindex(sim, 0, projection='XY', slice_level=160)
visu.vectorfield_color_by_fieldindex(sim, 0, projection='XZ', slice_level=0)
visu.vectorfield_color_by_fieldindex(sim, 0, projection='YZ', slice_level=0)


