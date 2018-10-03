#include <ctime>
#include <iostream>
#include <ros/ros.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/Image.h>
#include <image_transport/image_transport.h>
#include <raspicam/raspicam_cv.h>

using namespace std;
 
int main ( int argc,char **argv ) {
    
    ros::init(argc, argv, "left");
    
   // raspicam::RaspiCam_Cv Camera;
    cv::Mat image;
    
    raspicam::RaspiCam_Cv Camera;
    Camera.set( CV_CAP_PROP_FORMAT, CV_8UC1 );
    if (!Camera.open()) {cerr<<"Error opening the camera"<<endl;return -1;}
    ros::NodeHandle n;
    //set camera params
    image_transport::ImageTransport it(n);
    
    
    //Camera.set( CV_CAP_PROP_FORMAT, CV_8UC1 );
    
    image_transport::Publisher pub = it.advertise<std_msgs::String>("image", 1);
    
    ros::Rate loop_rate(40);
   
    while(ros::ok()) {
        Camera.grab();
        Camera.retrieve ( image);
        sensor_msgs::ImagePtr msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8", image).toImageMsg();
        pub.publish(msg);
        loop_rate.sleep();
    }
    Camera.release();

return 0;
}
