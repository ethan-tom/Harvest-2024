import numpy as np



class waypointBase:
    def __init__(self, lat, long):
        self.latitude = lat
        self.longitude = long


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

def line_checker(phi1, lambda1, theta13, phi2, lambda2, theta23):
    """
    Calculates geodetic quantities between two points on a sphere.

    Args:
        phi1 (float): Latitude of the first point in radians.
        lambda1 (float): Longitude of the first point in radians.
        theta13 (float): Initial bearing from the first point to the intersection point in radians.
        phi2 (float): Latitude of the second point in radians.
        lambda2 (float): Longitude of the second point in radians.
        theta23 (float): Initial bearing from the second point to the intersection point in radians.

    Returns:
        A tuple containing:
            - delta12: Angular distance between the two points.
            - theta12, theta21: Initial and final bearings between the two points.
            - alpha1, alpha2, alpha3: Angles of the triangle formed by the two points and the intersection point.
            - delta13: Angular distance between the first point and the intersection point.
            - phi3: Latitude of the intersection point.
            - lambda3: Longitude of the intersection point.
    """

    delta_phi = phi2 - phi1
    delta_lambda = lambda2 - lambda1

    delta12 = 2 * np.arcsin(np.sqrt(np.sin(delta_phi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2)**2))

    theta_a = np.arccos((np.sin(phi2) - np.sin(phi1) * np.cos(delta12)) / (np.sin(delta12) * np.cos(phi1)))
    theta_b = np.arccos((np.sin(phi1) - np.sin(phi2) * np.cos(delta12)) / (np.sin(delta12) * np.cos(phi2)))

    if np.sin(lambda2 - lambda1) > 0:
        theta12 = theta_a
        theta21 = 2 * np.pi - theta_b
    else:
        theta12 = 2 * np.pi - theta_a
        theta21 = theta_b

    alpha1 = theta13 - theta12
    alpha2 = theta21 - theta23
    alpha3 = np.arccos(-np.cos(alpha1) * np.cos(alpha2) + np.sin(alpha1) * np.sin(alpha2) * np.cos(delta12))

    delta13 = np.arctan2(np.sin(delta12) * np.sin(alpha1) * np.sin(alpha2), np.cos(alpha2) + np.cos(alpha1) * np.cos(alpha3))
    phi3 = np.arcsin(np.sin(phi1) * np.cos(delta13) + np.cos(phi1) * np.sin(delta13) * np.cos(theta13))
    delta_lambda13 = np.arctan2(np.sin(theta13) * np.sin(delta13) * np.cos(phi1), np.cos(delta13) - np.sin(phi1) * np.sin(phi3))
    lambda3 = lambda1 + delta_lambda13

    return delta12, theta12, theta21, alpha1, alpha2, alpha3, delta13, phi3, lambda3

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
        