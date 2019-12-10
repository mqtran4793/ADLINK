# ADLINK
Install OpenCV on Ubuntu

https://linuxconfig.org/install-opencv-on-ubuntu-18-04-bionic-beaver-linux

https://www.e-consystems.com/Articles/Camera/accessing_cameras_in_opencv_with_high_performance.asp

void CopyMat(cv::Mat &OutFrame, void *Buffer) {
	cv::Mat incomeMat(
		cv::Size(640, 480), CV_8UC2, Buffer);
	cv::cvtColor(incomeMat, m_cvMatBuffer, cv::COLOR_YUV2BGR_YUYV);
}
static void process_image(const void *p, int size)
{
	frame_number++;
	CopyMat(m_cvMatBuffer, (void *)p);
	cv::imshow("draw", m_cvMatBuffer);
	cv::waitKey(5);
}








import os
import cv2 as cv
import numpy as np

try:
    from openvino import inference_engine as ie
    from openvino.inference_engine import IENetwork, IEPlugin
except Exception as e:
    exception_type = type(e).__name__
    print("The following error happened while importing Python API module: \n[ {} ] {}".format(exception_type, e))
    sys.exit(1)

plugin_dir = None
model_xml = "handwritten.xml"
model_bin = "handwritten.bin"

plugin = IEPlugin("MYRIAD", plugin_dirs=plugin_dir)
net = IENetwork.from_ir(model=model_xml, weights=model_bin)

input_blob = next(iter(net.inputs))
output_blob = next(iter(net.outputs))
excec_net = plugin.load(network=net)
del net

def main():
    cap = cv.VideoCapture(0)

    if(cap.isOpened() == False):
        print("Error opening video stream or file")

    while(cap.isOpened()):
        (ret, frame) = cap.read()

        if ret == True:
            #cv.imshow("Video Captured", frame)

            processedImage = process_image(frame)

            res = excec_net.infer(inputs={input_blob: processedImage})
            
            print(res)

            if cv.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
        
    cap.release()
    cv.destroyAllWindows()

def process_image(img):
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #i = cv2.bitwise_not(i)
    cv.imshow('Image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    img = cv.resize(img, (28, 28))
    img = np.reshape(img, [1, 28, 28, 1])
    img = img.astype('float32')
    img = img / 255.0
    #print(new_model.predict(i))
    #print('Predicted label: ', new_model.predict_classes(i))
    #print('\n')
    return img

if __name__ == '__main__':
    main()
