#!/usr/bin/python
# coding: utf-8

r"""Generation script for ISO 4014 screw"""

from ccad.model import prism, filling, ngon, cylinder, translated

k_max = 1.525
s_max = 4.0
l_g_max = 6.0
d_s_max = 2.0
d_s_min = 1.86
l_max = 16.35

head = translated(prism(filling(ngon(2 / 3**.5 * s_max / 2., 6)), (0, 0, k_max)), (0., 0., -k_max))

threaded = cylinder(d_s_min / 2., l_max)
unthreaded = cylinder(d_s_max / 2., l_g_max)

part = head + threaded + unthreaded
anchors = {1: {"position": (0., 0., 0.),
               "direction": (0., 0., -1.),
               "dimension": d_s_max,
               "description": "screw head on plane"}}

if __name__ == '__main__':
    import ccad.display as cd
    v = cd.view()
    v.display(part, color=(0.1, 0.1, 1.0), transparency=0.3)
    for k, anchor in anchors.items():
        v.display_vector(origin=anchor['position'], direction=anchor['direction'])
    cd.start()
