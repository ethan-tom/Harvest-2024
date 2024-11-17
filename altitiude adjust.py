import numpy as np


class waypointBase:
    def __init__(self, lat, long):
        self.latitude = lat
        self.longitude = long
        
list_list_drones =[]
unusable=[]

def round_to_fifty(x):
    remainder = x % 50
    if remainder < 25:
        return x - remainder
    else:
        return x + (50 - remainder)

def  collisionAlert(drone):
	for x in list_drones:
		if  x.current_locat.latitude>  0.000538 +drone.current_locat.latitude or x.current_locat.latitude <  drone.current_locat.latitude-0.000538 :
			if  x.current_locat.longitude>  0.000538 +drone.current_locat.longitude or x.current_locat.longitude <  drone.current_locat.longitude-0.000538 :
				unusable.append(round_to_fifty(x.altitude))
		else :
			continue
	usables =[]
	for t in range(drone.up_ceiling,drone.lower_ceiling,50):
		usables.append(t)
	for x in unusable:
		usables.pop(x)
	try:
		drone.altitude_change(usables[0])
	except IndexError:
		change_azimuth()
	

