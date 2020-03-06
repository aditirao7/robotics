#!/usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix,Imu
from tf.transformations import euler_from_quaternion
import math
from std_msgs.msg import String
yaw=0
gps_angle=0
#import haversine
pointf=(49.9001891682,8.90004687712)
def callback1(data):
    global gps_angle
    lat1=data.latitude
    lon1=data.longitude
    lat2=49.9001891682
    lon2=8.90004687712
    lon_change = math.radians(lon2 - lon1)
    lat_change = math.radians(lat2 - lat1)
    x = math.sin(lon_change) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(lon_change))
    bearing = math.degrees(math.atan2(x, y))
    gps_angle = (bearing + 360)/360
    print(gps_angle-yaw)

def callback2(data2):
   global yaw
   quaternion=(data2.orientation.x,data2.orientation.y,data2.orientation.z,data2.orientation.w)
   euler=euler_from_quaternion(quaternion)
   yaw=math.degrees(euler[2])


def listener():
        try:
            rospy.init_node('gps','imu', anonymous=True)
            rospy.Subscriber("fix", NavSatFix, callback1)
            rospy.Subscriber("imu", Imu, callback2)
            rospy.spin()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    listener()
