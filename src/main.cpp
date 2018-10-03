#include <ctime>
#include <iostream>
#include <ros/ros.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/Image.h>
#include <image_transport/image_transport.h>
using namespace std;
 
int main ( int argc,char **argv ) {
    
    ros::init(argc, argv, "left");
    
   // raspicam::RaspiCam_Cv Camera;
    cv::Mat image;
    
    ros::NodeHandle n;
    //set camera params
    image_transport::ImageTransport it(n);
    
    VideoCapture cap(0);
    
    if(!cap.isOpened())  // check if we succeeded
    {
        std::cout << "Camera Init Fail\n";
        return -1;
    }
    
    std::cout << "Camera Init Successful\n";
    std::cout << "Setting parameters..\n";
    
    std::cout <<"\t[PARAM_FRAME_WIDTH] ";
    if(!cap.set(CV_CAP_PROP_FRAME_WIDTH,320)){
        std::cout <<"SUCCESS\n";
    }else{
        std::cout <<"FAIL\n";
    }
    
    std::cout <<"\t[PARAM_FRAME_HEIGHT] ";
    if(!cap.set(CV_CAP_PROP_FRAME_HEIGHT,240)){
        std::cout <<"SUCCESS\n";
    }else{
        std::cout <<"FAIL\n";
    }
    
    std::cout <<"\t[PARAM_FPS] ";
    if(!cap.set(CV_CAP_PROP_FPS,30)){
        std::cout <<"SUCCESS\n";
    }else{
        std::cout <<"FAIL\n";
    }
    
    int nFPS = cap.get(CV_CAP_PROP_FPS);
    std::cout << "Loaded FPS : " << nFPS << "\n";
    
    //Camera.set( CV_CAP_PROP_FORMAT, CV_8UC1 );
    
    image_transport::Publisher pub = it.advertise<std_msgs::String>("image", 1);
    
    ros::Rate loop_rate(40);
   
    while(ros::ok()) {
        cap >> image
        sensor_msgs::ImagePtr msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8", image).toImageMsg();
        pub.publish(msg);
        loop_rate.sleep();
    }
    Camera.release();

return 0;
}
