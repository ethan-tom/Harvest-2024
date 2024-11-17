import numpy as np
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from drone_classes import DroneBase
    from ethan1 import waypointBase

def line_constructor(pointA : waypointBase, pointB: waypointBase):
    deg_to_rad = np.pi/180
    rad_to_deg = 1/deg_to_rad
    r = 6371e3
    phi1 = pointA.latitude * deg_to_rad
    phi2 = pointB.latitude * deg_to_rad
    dphi = (pointA.latitude-pointB.latitude) * deg_to_rad
    dgamma = (pointA.longitude-pointB.longitude) * deg_to_rad
    # a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    # c = 2 ⋅ atan2( √a, √(1−a) )
    # d = R ⋅ c
    a = np.sin(dphi/2)**2+np.cos(phi1)*np.cos(phi2)*(np.sin(dgamma/2)**2)
    c = 2*np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distance = r*c
    # θ = atan2( sin Δλ ⋅ cos φ2 , cos φ1 ⋅ sin φ2 − sin φ1 ⋅ cos φ2 ⋅ cos Δλ )
    y=np.sin(dgamma)*np.cos(phi2)
    x=np.cos(phi1)*np.sin(phi2)-np.sin(phi1)*np.cos(phi2)*np.cos(dgamma)
    bearing = 360 - rad_to_deg*np.arctan2(y,x)
    return bearing, distance

import numpy as np

class LowLevelPath:
    def __init__(self, pointA, pointB):
        self.heading, self.legnth = line_constructor(pointA=pointA, pointB=pointB)


class PathBase:
    def __init__(self, pointA, pointB):
        self.point_a = pointA
        self.paint_B = pointB
        self.pathto = LowLevelPath(pointA, pointB)
        self.speed = 0
        self.pathfrom = LowLevelPath(pointB, pointA)
        self.counter = 10
    

    def setspeed(self, speed):
        self.speed= speed
    
    @property
    def timeto(self, speed):
        return self.pathto.legnth/speed 
    
    @property
    def timefrom(self, speed):
        return self.pathfrom.legnth/speed 
        