import numpy as np 
#cause why not
cmds={"emg_land_lat":0b000000,
      "emglandlong":0b000001,
      "qdest_fin_lat":0b000010,
      "qdest_fin_long":0b000011,
      "qloc_lat":0b000100,
      "qloc_long":0b000101,
      "q_airspd":0b000110,
      "qtype":0b000111,
      "qspdmax":0b001000,
      "r_freq_change":0b001001,
      "a_freq_change":0b001001,
      "dfreq_change":0b001011,
      "r_spd_change":0b001100,
      "a_spd_change":0b001101,
      "qscup":0b001110,
      "qsclow":0b001110,
      "q_load":0b010001,
      "r_change_br":0b010010,
      "a_change_br":0b010011,
      "mayday":0b010100,
      "wypnt_rchd":0b011000,
      "wypnt_unrchd":0b011001,
      "cllsn":0b011010,
      "req_dalt":0b011011, 
      "acc_dalt":0b011100,
      "query_alt":0b011101,
      "dat_resp": 0b011110, 
      "rsclow": 0b011111,
      "asclow": 0b100000,
      "dsclow": 0b100001,
      }
'''
lat and long is longitude and latitiude ,
emg is emergency ,
q is query ,
fin is final , 
r is request , 
a is accept , 
d is deny,
sc= service ceiling ,br=bearing,
wypnt is waypoint'''

cmd_set = ["qloc_lat", "qloc_long", "qtype", "q_airspd", "qscup", "q_load"]

def checkdata(drone, station_sdr):
      def createquerybit(cmdstr):
            return bitconstruct(cmd[cmdstr], drone.regnohash, 0b11)
      verify_set = [drone.type, drone.speed, drone.up_ceiling, drone.lower_ceiling]
      transmit(drone,0,cmd[cmd_set[0]], station_sdr)
      object = receive(drone, station_sdr)
      