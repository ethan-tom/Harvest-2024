from typing import TYPE_CHECKING, List
import numpy as np
if TYPE_CHECKING:
    from drone_classes import DroneBase
    from ethan1 import waypointBase
    from paths import PathBase

list_drones : List[DroneBase] = list()  
list_paths: List[PathBase] = list() 
list_wpnts: List[waypointBase] = list() 

def dummy_constructor(i):
    return DroneBase()

for i in range(100):
    list_drones.append(dummy_constructor(i))

def is_colliding(oldpath):
    pA, pB = oldpath.point_a, oldpath.point_b
    ph1, lm1 = (pA.latitude, pA.longitude)*np.pi/180
    for close in close_paths(pA, list_paths):
        ph2, lm2 = (close.latitude, close.longitude)*np.pi/180
        th13 = oldpath.bearing
        th23 = 
        try:
            _, _, _, line_checker(ph1, lm1, th13, ph2, lm2, th23)
        except BaseException:
            
        



