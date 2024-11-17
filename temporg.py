from typing import TYPE_CHECKING, List
import numpy as np
if TYPE_CHECKING:
    from drone_classes import DroneBase
    from paths import waypointBase
from paths import PathBase

list_drones : List[DroneBase] = list()  
list_paths: List[PathBase] = list() 
list_wpnts: List[waypointBase] = list() 

def dummy_constructor(i):
    return DroneBase()

# for i in range(100):
#     list_drones.append(dummy_constructor(i))

def is_coliding(path):
    for closedrone in closest(list_drones, path.point_a):
        if doIntersect(closedrone.current_locat, closedrone.current_path.paint_B, path.paint_B, path.point_a):
            return True
    return False

def pathset(drone, pointB):
    drone.paths_used.append(drone.current_path)   
    drone.current_path(PathBase(drone.current_locat, pointB))

        



