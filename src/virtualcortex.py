import rospy
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo

from cv_bridge import CvBridge, CvBridgeError

def yaml_to_CameraInfo(yaml_fname):
    """
    Parse a yaml file containing camera calibration data (as produced by
    rosrun camera_calibration cameracalibrator.py) into a
    sensor_msgs/CameraInfo msg.

    Parameters
    ----------
    yaml_fname : str
        Path to yaml file containing camera calibration data
    Returns
    -------
    camera_info_msg : sensor_msgs.msg.CameraInfo
        A sensor_msgs.msg.CameraInfo message containing the camera calibration
        data
    """
    # Load data from file
    with open(yaml_fname, "r") as file_handle:
        calib_data = yaml.load(file_handle)
    # Parse
    camera_info_msg = CameraInfo()
    camera_info_msg.width = calib_data["image_width"]
    camera_info_msg.height = calib_data["image_height"]
    camera_info_msg.K = calib_data["camera_matrix"]["data"]
    camera_info_msg.D = calib_data["distortion_coefficients"]["data"]
    camera_info_msg.R = calib_data["rectification_matrix"]["data"]
    camera_info_msg.P = calib_data["projection_matrix"]["data"]
    camera_info_msg.distortion_model = calib_data["distortion_model"]
    return camera_info_msg


def talker():
        pub = rospy.Publisher('left/image_raw', Image, queue_size=1)
        pubinfo = rospy.Publisher('left/camera_info', CameraInfo, queue_size=10)
        rospy.init_node('left', anonymous=False)
        rate = rospy.Rate(40)
        camera = PiCamera()
        camera.resolution = (1280, 960)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(1280, 960))
        time.sleep(0.1)
        yaml = yaml_to_CameraInfo('camera.yaml')
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text

                image = frame.array
                bridge = CvBridge()
                pubinfo.publish(yaml);
                pub.publish(bridge.cv2_to_imgmsg(image, "bgr8"))
                rawCapture.truncate(0)
                if(rospy.is_shutdown()):
                    break



if __name__ == '__main__':
    try:


           talker()
    except rospy.ROSInterruptException:
           pass
