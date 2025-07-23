import rospy
from clover import srv
from std_srvs.srv import Trigger
import math
from clover.srv import SetLEDEffect


rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
set_effect = rospy.ServiceProxy('led/set_effect', SetLEDEffect)  # define proxy to ROS-service
land = rospy.ServiceProxy('land', Trigger)


def navigate_wait(x=0, y=0, z=1, speed=0.5, frame_id='', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)
    rospy.sleep(1.5)

def mushroom(y1):     # Гриб
    navigate_wait(frame_id="aruco_map", x=1,y=y1, z=1)
    navigate_wait(frame_id="aruco_map", x=1,y=y1, z=1.5)
    navigate_wait(frame_id="aruco_map", x=2,y=y1, z=1.7)
    navigate_wait(frame_id="aruco_map", x=0.5,y=y1, z=1.7)
    navigate_wait(frame_id="aruco_map", x=1,y=y1, z=2.5)
    navigate_wait(frame_id="aruco_map", x=2,y=y1, z=3)
    navigate_wait(frame_id="aruco_map", x=2.75,y=y1, z=2.5)
    navigate_wait(frame_id="aruco_map", x=3.5,y=y1, z=1.7)
    navigate_wait(frame_id="aruco_map", x=2.75,y=y1, z=1.7)
    navigate_wait(frame_id="aruco_map", x=2.75,y=y1, z=1.25)
    navigate_wait(frame_id="aruco_map", x=1,y=y1, z=1)

def star(y2):     #Звезда
    navigate_wait(frame_id="aruco_map", y=y2, x=1)
    navigate_wait(frame_id="aruco_map", z=3.5, y=y2,x=2)
    navigate_wait(frame_id="aruco_map", x=3,y=y2)
    navigate_wait(frame_id="aruco_map", z=2.5,x=0.5,y=y2)
    navigate_wait(frame_id="aruco_map", z=2.5,x=3.5,y=y2)
    navigate_wait(frame_id="aruco_map", x=1,y=y2)



set_effect(r=0, g=0, b=255)
navigate_wait(frame_id="body",speed=1,auto_arm=True)

set_effect(r=255, g=255, b=0)
star(6)

set_effect(r=128, g=0, b=128)
mushroom(6)

set_effect(r=255, g=0, b=0)
navigate_wait(frame_id="aruco_map",speed=2)

navigate_wait(frame_id="aruco_map", x=0,y=0)
land()

