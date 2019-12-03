#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include <IoTDataThing.hpp>
#include <JSonThingAPI.hpp>
#include <thing_IoTData.h>
#include <ThingAPIException.hpp>

using namespace std;
using namespace com::adlinktech::datariver;
using namespace com::adlinktech::iot;
 
using namespace std;
using namespace cv;
 
int main(){
 
  // Create a VideoCapture object and open the input file
  // If the input is the web camera, pass 0 instead of the video file name
  VideoCapture cap(0); 
    
  // Check if camera opened successfully
  if(!cap.isOpened()){
    cout << "Error opening video stream or file" << endl;
    return -1;
  }
     
  // while(1){
 
    Mat frame;
    Mat frame_gray;
    
    // Capture frame-by-frame
    cap >> frame;
    cvtColor(frame, frame_gray, COLOR_RGB2GRAY);
    // If the frame is empty, break immediately
    // if (frame.empty())
      // break;
 
    // Display the resulting frame
    // imshow( "Frame", frame );
    frame_gray = frame_gray.reshape(1, 1);
    cout << frame_gray.row(0).total() << endl;
 
    // Press  ESC on keyboard to exit
    // char c=(char)waitKey(25);
    // if(c==27)
      // break;
  // }
  
  // When everything done, release the video capture object
  cap.release();
 
  // Closes all the frames
  destroyAllWindows();
     
  return 0;
}
