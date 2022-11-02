from __future__ import print_function

import time,math
from sr.robot import *

"""
Exercise 3 python script

We start from the solution of the exercise 2
Put the main code after the definition of the functions. The code should make the robot:
	- 1) find and grab the closest silver marker (token)
	- 2) move the marker on the right
	- 3) find and grab the closest golden marker (token)
	- 4) move the marker on the right
	- 5) start again from 1

The method see() of the class Robot returns an object whose attribute info.marker_type may be MARKER_TOKEN_GOLD or MARKER_TOKEN_SILVER,
depending of the type of marker (golden or silver). 
Modify the code of the exercise2 to make the robot:

1- retrieve the distance and the angle of the closest silver marker. If no silver marker is detected, the robot should rotate in order to find a marker.
2- drive the robot towards the marker and grab it
3- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
4- retrieve the distance and the angle of the closest golden marker. If no golden marker is detected, the robot should rotate in order to find a marker.
5- drive the robot towards the marker and grab it
6- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
7- start again from 1

	When done, run with:
	$ python run.py exercise3.py

"""


a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()
""" instance of the class Robot"""
def sign(a):
    if(a>0):
        return 1
    else:
        return -1
def CTM(val):#Convert To Meters
    return val * 81.6360436665


def GAGTM(Flag):#GoAndGrabTheNearestMarker
    
    while(True):
        CToken = NSAM(Flag)
        while(CToken[1] > a_th or CToken[1] < -a_th):
            turn(sign(CToken[1]-a_th) * 10,0.05)
            CToken = NSAM(Flag)
        e_po = CToken[0]- d_th
        while(CToken[0] > d_th):
            e_p = CToken[0]- d_th
            drive(400*(e_p) - 100*(e_p - e_po),0.05)
            CToken = NSAM(Flag)
            e_po = e_p
        
        time.sleep(0.5)
        if(CToken[0] < d_th):
            break
        else:
            exit()

def drive(speed,seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def rotate(speed,angle):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    t = CTM(R.width) * ((angle/(180/math.pi))/speed)
    R.motors[0].m0.power = speed 
    R.motors[0].m1.power = 0 
    print(t) 
    time.sleep(t)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
def NSAM(Flag):
    dist=100
    
    for token in R.see():
        if token.dist < dist and token.info.marker_type == Flag:
            dist=token.dist
            rot_y=token.rot_y
    if dist==100:
	    return -1
    else:
   	    return dist,rot_y

def RR():
    turn(10,0.3)

def RL():
    turn(-10,0.3)


def DBTM(m1,m2):#d = r1 + r - 2 * r1r2cos(theta2-theta1)
    r1 = m1.centre.polar.length
    theta1 = m1.centre.polar.rot_y
    r2 = m2.centre.polar.length
    theta2 = m2.centre.polar.rot_y

    return math.sqrt(r1**2 + r2**2 - 2*r1*r2*math.cos(CTR(theta2-theta1)))


def LFSM():#Look For Silver Marker
    GAGTM(MARKER_TOKEN_SILVER)
    R.grab()
    for i in range(7):
        RR()
    drive(50,2)
def LFGM():
    GAGTM(MARKER_TOKEN_GOLD)
    R.release()
    for i in range(7):
        RL()
def CTR(angle):#Convert To Radians
    return angle *(math.pi/180)
def main():
    i = 0
    Flags = [MARKER_TOKEN_SILVER , MARKER_TOKEN_GOLD]
    StringF = ["Silver","Golden"]
    while(1):
        while(NSAM(MARKER_TOKEN_SILVER)<0):
            print("looking for a Silver marker")
            RL()
        LFSM()
        LFGM()#Move It To The Right
        i+=1

main()



