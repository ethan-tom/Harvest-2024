import numpy as np

class waypointBase:
    def _init_(self, lat, long):
        self.latitude = lat
        self.longitude = long

def main(self,phi1,phi2,gamma1,gamma2,theta1,theta2):
	dphi=phi1-phi2
	dgamma=gamma1-gamma2
	temp=np.sqrt(np.sin(dphi/2)**2 +np.cos(phi2)*np.sin(dgamma/2))
	rho=2*np.arctan(temp)
	#:	δ12 = 2⋅asin( √(sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)) )
	temp2=(np.sin(phi2)-np.sin(phi1)*np.cos(rho))/(np.sin(rho)*np.cos(phi1))
	temp3=(np.sin(phi1)-np.sin(phi2)*np.cos(rho))/(np.sin(rho)*np.cos(phi2))
	thetaa=np.arccos(temp2)
	thetab=np.arccos(temp3)
		#   θa = acos( ( sin φ2 − sin φ1 ⋅ cos δ12 ) / ( sin δ12 ⋅ cos φ1 ) )
		# θb = acos( ( sin φ1 − sin φ2 ⋅ cos δ12 ) / ( sin δ12 ⋅ cos φ2 ) )
	if(np.sin(gamma2-gamma1)>0):
		theta12=thetaa
		theta21=2*np.pi-thetab
	else:
		theta21=thetab
		theta12=2*np.pi-thetaa
	alpha1=theta1-theta12
	alpha2=theta21-theta2
	if (np.sin(alpha1)==0 and np.sin(alpha2)==0):
		altitude=altitude+20
	else :
	# α3 = acos( −cos α1 ⋅ cos α2 + sin α1 ⋅ sin α2 ⋅ cos δ12 )
		temp4=(-np.cos(alpha1)*np.cos(alpha2)+np.sin(alpha1)*np.sin(alpha2)*np.cos(rho))
		alpha3=np.arccos(temp4)
		# δ13 = atan2( sin δ12 ⋅ sin α1 ⋅ sin α2 , cos α2 + cos α1 ⋅ cos α3 )
		rho13=np.arctan(np.sin(rho)*np.sin(alpha1)*np.sin(alpha2),np.cos(alpha2)+np.cos(alpha1)*np.cos(alpha3))**2
		# φ3 = asin( sin φ1 ⋅ cos δ13 + cos φ1 ⋅ sin δ13 ⋅ cos θ13 )
		phi3=np.arcsin(np.sin(phi1)*np.sin(rho13)+np.cos(phi1)*np.sin(rho13)* np.cos(theta1))
		# Δλ13 = atan2( sin θ13 ⋅ sin δ13 ⋅ cos φ1 , cos δ13 − sin φ1 ⋅ sin φ3 )
		dgamma13=np.arctan(np.sin(theta1)*np.sin(rho13)*np.cos(phi1),np.cos(rho13)-np.sin(phi1)*np.sin(phi3))**2
		gamma2=gamma1+dgamma13



