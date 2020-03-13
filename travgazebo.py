#!/usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix,Imu
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion
import math
from std_msgs.msg import String
from pyproj import Geod
#from haversine import haversine, Unit
lat1=0
lon1=0
yaw=0
lat2=49.9000116568
lon2=8.90000071435
def callback1(data):
    global lat1
    global lon1
    lat1=data.latitude
    lon1=data.longitude

def callback2(data2):
   global yaw
   quaternion=(data2.orientation.x,data2.orientation.y,data2.orientation.z,data2.orientation.w)
   euler=euler_from_quaternion(quaternion)
   yaw=math.degrees(euler[2])+180
   yaw=abs(yaw-360)


def listener():
            rospy.init_node('gps','imu', anonymous=True, disable_signals=True)
            rospy.Subscriber("fix", NavSatFix, callback1)
            rospy.Subscriber("imu", Imu, callback2)
            pub=rospy.Publisher("cmd_vel", Twist)
            global msg
            msg=Twist()
            while 1:
                geodesic=Geod(ellps='WGS84')
                bearing, reverse_bearing, distance=geodesic.inv(lon1, lat1, lon2,lat2)
                angle=yaw-(bearing)
                print("Distance:", distance)
                print(angle)
                if(angle>1):
                    if (angle< 181):
                        print("Turn right")
                        msg.angular.z=1
                    elif (angle > 179):
                        print("Turn left")
                        msg.angular.z=-1
                if(angle<-1):
                    angle=abs(angle)
                    if (angle > 179):
                       print("Turn right")
msg.angular.z=1
                    elif (angle < 181):
                       print("Turn left")
                       msg.angular.z=-1
                elif(angle<=1 and angle>=-1):
                    print("Move straight")
                    while(distance>0.1):
                        print('move forward')
                        msg.angular.z=0
                        msg.linear.x=-1
                pub.publish(msg)

            rospy.spin()
if __name__ == '__main__':
    listener()
                       
