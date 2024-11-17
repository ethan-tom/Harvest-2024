import numpy as np
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ethan1 import waypointBase
    from paths import PathBase


# all distances in meters, heights in meters, speeds in meters per second and times in seconds
class DroneBase:
    def __init__(self, locat_curr, path_curr):
        self.freq = 400e6
        self.paths_used : List[PathBase]= list()
        self.bearing = 0.0
        self.speed = 4
        self.altitude = 300
        self.up_ceiling = 1200  # TODO: add adaptive upper ceiling based on drone type and usage
        self.lower_ceiling = 200 # TODO: add adaptive lower ceiling based on city topography
        self.emergency_speed = 5 # TODO: add adaptive emergency power based on drone type and usage
        self.max_speed = 4 # TODO: add adaptive max speed based on drone type and usage
        self.priority = 0
        self.load_type = 0 # indexing : 0 - general purpose, 1 - transport, 2 - security, 3 - high piority transport
        self.current_locat : waypointBase = locat_curr
        self.current_path : PathBase = path_curr
        self.regno = int(np.loadtxt("reginfo.txt")[0])
        self.regnohash = hash(self.regno)
        self.flight_type = 0 # indexing : 0 - Multirotor, 1 - heavy multirotor, 2- fixed wing, 3- single rotor
        self.max_accel_linear = 1
        self.max_turn_rate = 30 # in deg/s

    
    def set_path(self, newpath):
        if is_coliding(newpath):
            raise BaseException()
        list_paths.append(newpath)
        if newpath.speed>self.max_speed:
            raise SystemExit()
        if not newpath==self.path:
            self.path = newpath
    
    def altitude_change(self, new_alt, station_sdr):
        if new_alt>self.up_ceiling or new_alt<self.lower_ceiling:
            raise SystemExit()
        while 0:
            transmit(self, new_alt, cmds["req_dalt"], station_sdr)

