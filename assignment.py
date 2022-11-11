from __future__ import print_function

import time,math
from sr.robot import *


history = {"Silver":[],"Golden":[]}#dict to keep track of the marker that are already paired 
StringF = ["Silver","Golden"] # variable that helpes in encoding the colored into binary system
Flags = {"Silver":MARKER_TOKEN_SILVER , "Golden":MARKER_TOKEN_GOLD}#mapping between encoding and the flags 


a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()
""" instance of the class Robot"""

#                                   Helper Functions
def sign(a):
    """
    helper function to check the sign of the number a 
    """
    if(a>0):
        return 1
    else:
        return -1
def CTM(distance):
    """
    helper function to convert distance to meters
    """
    return distance * 81.6360436665

def CTR(angle):
    """
    helper function to convert angles to radians
    """
    return angle *(math.pi/180)

#                                   End Helper Functions

#                                   Given Functions

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

#                                   End Given Functions

#                                   My Functions

def GAGTM(iter):#GoAndGrabTheNearestMarker
    if(iter!= 0 and iter!=1):
        iter = iter%2 # in case the number was not transformed to modulus of 2
    """
    function to go to the desired marker 
    Args: 
        iter: a number between 0 (for Silver Box) and 1 (for Golden Box)
    """
    global history
    CToken = NNPB(iter)
    # rotating to face the box by driving the error of orientation to 0 (used P controler)
    while(CToken[1] > a_th or CToken[1] < -a_th):
        turn(sign(CToken[1]-a_th) * 10,0.05)
        CToken = NNPB(iter)
    
    # going to the box by driving the error of distance to 0 (used PD controler)
    e_po = CToken[0]- d_th
    while(CToken[0] > d_th):
        e_p = (CToken[0]- d_th)/0.05
        drive(500*(e_p) - 200*(e_p - e_po),0.05)
        CToken = NNPB(iter)
        if(CToken == -1):
            return -1
        e_po = e_p
    
        if(CToken[0] < 1.5*d_th and iter==1):
            time.sleep(0.5)
            R.release()
            history["Golden"].append(CToken[2])
            break
        if(CToken[0] < d_th and iter==0):
            time.sleep(0.5)
            R.grab()
            history["Silver"].append(CToken[2])
            break
        



def rotate(speed,angle):
    """
    Function for rotating to the desired angle
    
    Args:   speed (int): the speed of the wheels
	        angle (int): the desired angle in degrees
    """
    t = CTM(R.width) * ((angle/(180/math.pi))/speed)
    turn(speed/2, t)



def NNPB(iter):
    """
    The name of function is short for Nearest Non Paired Box
    the function basically looks for the nearest box that is not visited yet
    Args: 
        iter: a number between 0 (for Silver Box) and 1 (for Golden Box)  
    """
    if(iter!= 0 and iter!=1):
        iter = iter%2 # in case the number was not transformed to modulus of 2
    
    global history
    global Flags
    dist=100
    # look in the list of visible boxes for boxes that are
    # the nearest and 
    # the desired color and
    # not been visited yet  
    for token in R.see():
        if token.dist < dist and token.info.marker_type == Flags[StringF[iter]]\
                            and token.info.code not in history[StringF[iter]]:
            dist=token.dist
            rot_y=token.rot_y
            code = token.info.code
    if dist==100:
        return -1
    else:
   	    return dist,rot_y,code



def main():
    iter = 0
    global StringF
    global history #keep track of the box that has been already paired
    while(len(history["Golden"])<6):# repeate untill we run out of golden box
        while(NNPB(iter%2)<0):#try to find Silver and then golden box 
            print("looking for a "+StringF[iter%2]+" marker") 
            turn(-10,0.3)# Keep turning left untill finding the desired box
        
        if(GAGTM(iter%2) == -1):#Go And Grab/release a silver box
            continue
        
        if(iter%2==0):#only if we are looking for a silver box
            """ 
            this is to avoid running on a silver box on the way and to go to the 
            nearest golden box, because in this case the nearest golden box is on the outer circle
            """
            rotate(60,90) 
        iter+=1# this variable is needed to alternate between the colors of the boxes
    drive(-50,2)
    print("I finished :)")
    exit()
#                                   End My Functions

main()