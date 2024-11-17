import numpy as np
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ethan1 import waypointBase
    from paths import PathBase


# all distances in meters, heights in meters, speeds in meters per second and times in seconds
class DroneBase:
    def __init__(self, locat_curr, path_curr: PathBase, maxspeed = 0, final_dest):
        self.up_ceiling = 1200  # TODO: add adaptive upper ceiling based on drone type and usage
        self.lower_ceiling = 200 # TODO: add adaptive lower ceiling based on city topography
        self.emergency_speed = 5 # TODO: add adaptive emergency power based on drone type and usage
        self.max_speed = maxspeed # TODO: add adaptive max speed based on drone type and usage
        path_curr.setspeed(self.max_speed)
        self.freq = 400e6
        self.paths_used : List[PathBase]= list()
        self.bearing = 0.0
        self.speed = path_curr.speed
        self.altitude = 300
        self.truespeed = 0
        self.priority = 0
        self.load_type = 0 # indexing : 0 - general purpose, 1 - transport, 2 - security, 3 - high piority transport
        self.current_locat : waypointBase = locat_curr
        self.current_path : PathBase = path_curr
        self.regno = int(np.loadtxt("reginfo.txt")[0])
        self.regnohash = hash(self.regno)
        self.flight_type = 0 # indexing : 0 - Multirotor, 1 - heavy multirotor, 2- fixed wing, 3- single rotor
        self.max_accel_linear = 1
        self.max_turn_rate = 30 # in deg/s
        self.max_climb = 0.1 # in m/s 
        self.final_dest = final_dest

    
    def set_path(self, newpath):
        try:
            if is_coliding(newpath):
                list_paths.append(newpath)
        except collisionException():
            pass

        if newpath.speed>self.max_speed:
            raise overspeedAlert()
        if not newpath==self.path:
            self.path = newpath
    
    def altitude_change(self, new_alt, station_sdr):
        if new_alt>self.up_ceiling or new_alt<self.lower_ceiling:
            raise SystemExit()
        while not receive(self, station_sdr)==(bitconstruct(cmds["acc_dalt", self.regnohash, 0b11, 0, 0, 0])):
            transmit(self, new_alt, cmds["req_dalt"], station_sdr)
        self.altitude=new_alt

    def bearing_change(self, station_sdr, new_br):
        while not (receive(self,station_sdr)==bitconstruct(cmds["a_change_br", self.regnohash, 0b11, 0, 0, 0])):
            transmit(self, new_br, cmds["r_change_br"], station_sdr)
        self.bearing=new_br
    
    def speed_change(self, station_sdr, new_spd):
        while not (receive(self, station_sdr)==bitconstruct(cmds["a_spd_change", self.regnohash, 0b11, 0, 0, 0])):
            transmit(self, new_spd, cmds["r_spd_change"], station_sdr)
        self.speed=new_spd
    
    def updateall(self, station_sdr):
        if isNearby(self.currentpath.pointB, self):
            self.set_path(PathBase(self.current_loccat, self.final_dest))
        self.bearing = self.current_path.pathto.heading
        while not receive(self, station_sdr)==(bitconstruct(cmds["a_change_br", self.regnohash, 0b11, 0, 0, 0])):
            transmit(self, self.bearing, cmds["r_change_br"], station_sdr)
        while not receive(self, station_sdr)==(bitconstruct(cmds["a_spd_change", self.regnohash, 0b11, 0, 0, 0])):
            transmit(self, self.current_path.speed, cmds["r_spd_change"], station_sdr)
        try:
            new = checkdata(self, station_sdr)
        except badRfAlert():
            self.altitude_change(self.altitude, station_sdr)
            self.bearing_change(self.bearing, station_sdr)
            self.flight_type = new[0]
            self.load_type = new[1]
            self.speed=self.current_path.speed
            self.truespeed = new[2]
        except badInfoAlert():
            pass
        
        

        

        


