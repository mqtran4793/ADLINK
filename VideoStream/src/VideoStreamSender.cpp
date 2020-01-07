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

cv::Mat frame;
cv::Mat frame_gray;

class VideoStreamSender {
private:
    string m_thingPropertiesUri;
    DataRiver m_dataRiver = createDataRiver();
    Thing m_thing = createThing();

    DataRiver createDataRiver() {
        return DataRiver::getInstance();
    }

    Thing createThing() {
        // Create and Populate the TagGroup registry with JSON resource files.
        JSonTagGroupRegistry tgr;
        tgr.registerTagGroupsFromURI("file://definitions/TagGroup/com.adlinktech.MQ/VideoStreamTagGroup.json");
        m_dataRiver.addTagGroupRegistry(tgr);

        // Create and Populate the ThingClass registry with JSON resource files.
        JSonThingClassRegistry tcr;
        tcr.registerThingClassesFromURI("file://definitions/ThingClass/com.adlinktech.MQ/VideoStreamSenderThingClass.json");
        m_dataRiver.addThingClassRegistry(tcr);

        // Create a Thing based on properties specified in a JSON resource file.
        JSonThingProperties tp;
        tp.readPropertiesFromURI(m_thingPropertiesUri);
        return m_dataRiver.createThing(tp);
    }

    // void writeSample(void *frame) {
    //     IOT_VALUE frame_v;
    //     frame_v.iotv_byte_seq(*frame);

    //     IOT_NVP_SEQ sensorData = {
    //         IOT_NVP(string("video"), frame_v),
    //     };

    //     m_thing.write("video", sensorData);
    // }

public:
    VideoStreamSender(string thingPropertiesUri) :m_thingPropertiesUri(thingPropertiesUri) {
        cout << "Video Stream Sender started" << endl;
    }

    ~VideoStreamSender() {
        m_dataRiver.close();
        cout << "Video Stream Sender stopped" << endl;
    }

    int run(int runningTime) {
      // Create a VideoCapture object and open the input file
      // If the input is the web camera, pass 0 instead of the video file name
      cv::VideoCapture cap(0); 

      // Check if camera opened successfully
      if(!cap.isOpened()){
        cout << "Error opening video stream or file" << endl;
        return -1;
      }

      while (1) {
        // Capture frame-by-frame
        cap >> frame;
        cvtColor(frame, frame_gray, cv::COLOR_RGB2GRAY);
        // If the frame is empty, break immediately
        // if (frame.empty())
          // break;
    
        // Display the resulting frame
        // imshow( "Frame", frame );
        frame_gray = frame_gray.reshape(1, 1);
        // cout << frame_gray << endl;
    
        // Press  ESC on keyboard to exit
        // char c=(char)waitKey(25);
        // if(c==27)
          // break;
      // }
        // writeSample(&frame_gray);

        IOT_VALUE frame_v;
        frame_v.iotv_byte_seq(frame_gray);

        IOT_NVP_SEQ sensorData = {
            IOT_NVP(string("video"), frame_v),
        };

        m_thing.write("video", sensorData);
      }
      // When everything done, release the video capture object
      cap.release();
    
      // Closes all the frames
      cv::destroyAllWindows();

      return 0;
    }
};

int main(int argc, char *argv[]){
  // Get thing properties URI from command line parameter
    if (argc < 3) {
        cerr << "Usage: " << argv[0] << " THING_PROPERTIES_URI RUNNING_TIME" << endl;
        exit(1);
    }
    string thingPropertiesUri = string(argv[1]);
    int runningTime = atoi(argv[2]);

    try {
        // Create the Thing
        VideoStreamSender(thingPropertiesUri).run(runningTime);
    }
    catch (ThingAPIException& e) {
        cerr << "An unexpected error occurred: " << e.what() << endl;
    }catch(std::exception& e1){
        cerr << "An unexpected error occurred: " << e1.what() << endl;
    }
     
  return 0;
}
