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
	char filename[15];
	sprintf(filename, "frame-%d.raw", frame_number);
	FILE *fp=fopen(filename,"wb");
	if (out_buf)
		fwrite(p, size, 1, fp);
	fflush(fp);
	fclose(fp);
	
	// CopyMat(m_cvMatBuffer, (void *)p);
	// cv::imshow("draw", m_cvMatBuffer);
	// cv::waitKey(5);
		//cv::resizeWindow("draw", width, height);

	CopyMat(m_cvMatBuffer, (void *)p);
	cv::imshow("draw", m_cvMatBuffer);
	cv::waitKey(5);
		//cv::resizeWindow("draw", width, height);
}
