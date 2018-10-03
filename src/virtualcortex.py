import rospy
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from cv_bridge import CvBridge, CvBridgeError

def talker():
        pub = rospy.Publisher('image_raw', Image, queue_size=1)
        rospy.init_node('left')
        rate = rospy.Rate(40)
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(640, 480))
        time.sleep(0.1)
        while not rospy.is_shutdown():
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text

                image = frame.array
                bridge = CvBridge()
                pub.publish(bridge.cv2_to_imgmsg(image, "bgr8"))
                rawCapture.truncate(0)

if __name__ == '__main__':
    try:
           talker()
    except rospy.ROSInterruptException:
           pass
