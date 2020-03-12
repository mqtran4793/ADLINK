#!/usr/bin/env python

#
#                           ADLINK Edge SDK
#  
#     This software and documentation are Copyright 2018 to 2019 ADLINK
#     Technology Limited, its affiliated companies and licensors. All rights
#     reserved.
#  
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#  
#         http://www.apache.org/licenses/LICENSE-2.0
#  
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#

'''
This code is part of example scenario 1 'Connect a Sensor' of the
ADLINK Edge SDK. For a description of this scenario see the
'Edge SDK User Guide' in the /doc directory of the Edge SDK instalation.

For instructions on running the example see the README
file in the Edge SDK installation directory.
'''

from __future__ import print_function
import argparse
import sys
import os
import time
import random
from adlinktech.datariver import DataRiver, JSonTagGroupRegistry, JSonThingClassRegistry, JSonThingProperties
from adlinktech.datariver import IotValue, IotNvp, IotNvpSeq
import numpy as np
import cv2
import imutils

SAMPLE_DELAY_MS = 100

'''
Returns an absolute file uri of a given relative file path.
Allows to run this example from any location
'''
def get_abs_file_uri(filepath):
    dirpath = os.path.dirname(os.path.abspath(__file__))
    return 'file://' + str(os.path.join(dirpath, filepath))

class VideoStreamSender(object):
    
    # Initializing
    def __init__(self, thing_properties_uri):
        self._thing_properties_uri = thing_properties_uri
        
        self._dr = None
        self._thing = None
        self._send_payload = None
    
    # Enter the runtime context related to the object
    def __enter__(self):
        self._dr = DataRiver.get_instance()
        self._thing = self.create_thing()
        
        print('Video Stream sender started')
        
        return self
    
    # Exit the runtime context related to the object
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._dr is not None:
            self._dr.close()
        print('Video Stream sender stopped')
        
    def create_thing(self):
        # Create and Populate the TagGroup registry with JSON resource files.
        tgr = JSonTagGroupRegistry()
        tgr.register_tag_groups_from_uri(get_abs_file_uri('definitions/TagGroup/com.adlinktech.MQ/VideoStreamTagGroup.json'))
        self._dr.add_tag_group_registry(tgr) 
 
        # Create and Populate the ThingClass registry with JSON resource files.
        tcr = JSonThingClassRegistry()
        tcr.register_thing_classes_from_uri(get_abs_file_uri('definitions/ThingClass/com.adlinktech.MQ/VideoStreamSenderThingClass.json'))
        self._dr.add_thing_class_registry(tcr)
 
        # Create a Thing based on properties specified in a JSON resource file.
        tp = JSonThingProperties()
        tp.read_properties_from_uri(self._thing_properties_uri)
        return self._dr.create_thing(tp)
    
    def init_payload(self, video):
        payload = IotValue()
        payload.byte_seq = []
        #payload.byte_seq.append(video)
        #payload.byte_seq = video
        
        for i in video:
            #for j in i:
                #for k in j:
            payload.byte_seq.append(int(i))
        
        #print(len(video))
        self._send_payload = IotNvpSeq()
        self._send_payload.append(IotNvp('video', payload))

    def write_sample(self, video):
        self.init_payload(video)
        self._thing.write('video', self._send_payload)
        
    def run(self):
        #random.seed()
        #sample_count = (float(running_time) * 1000.0) / SAMPLE_DELAY_MS
        #actual_temperature = 21.5
        
        # Create a VideoCapture object and read from input file
        # If the input is the camera, pass 0 instead of the video file name
        cap = cv2.VideoCapture(0)
        #path = r'/home/adlink/Desktop/220px-SNice.svg.png'
        #img = cv2.imread('Smiley Face.jpg',-1)
        # Check if camera opened successfully
        if (cap.isOpened()== False): 
            print("Error opening video stream or file")

        #if f.mode == "r":
        #while sample_count > 0:
        #print(type(img[0][0][0]))
        #cv2.imshow('Image',img)
        #cv2.waitKey(0)
        #while True:
            #self.write_sample(img)
        
        while (cap.isOpened()):
             # Capture frame-by-frame
            (ret, frame) = cap.read()

            if ret == True:
                #frame = imutils.resize(frame, width=10)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #frame = np.dstack([frame, frame, frame])
                # Display the resulting frame
                #cv2.imshow('Frame',frame)
                #print(len(frame))
                # Press Q on keyboard to  exit
                #if cv2.waitKey(25) & 0xFF == ord('q'):
                    #break
                #print(len(frame[0]))
            # Break the loop
            #else: 
                #break
                frame = np.reshape(frame, (307200))
                #print(frame)
                self.write_sample(frame)
                
                #print(frame)
            
            #time.sleep(SAMPLE_DELAY_MS/1000.0)
        # When everything done, release the video capture object
            else:
                break
        cap.release()
        
        # Closes all the frames
        cv2.destroyAllWindows()

def main():
    # Get thing properties URI from command line parameter
    parser = argparse.ArgumentParser()
    parser.add_argument('running_time', type=int, nargs='?',
                        help='Total running time of the program (in seconds)',
                        default=60)
    parser.add_argument('thing_properties_uri', type=str, nargs='?',
                        help='URI of the thing properties file',
                        default='file://./config/VideoStreamSenderProperties.json')
    args = parser.parse_args()
    
    try:
        # Create the Thing
        video_send = VideoStreamSender(args.thing_properties_uri)
        # The 'with' statement supports a runtime context which is implemented
        # through a pair of methods executed (1) before the statement body is 
        # entered (__enter__()) and (2) after the statement body is exited (__exit__())
        with video_send as vidsend:
            vidsend.run()
    except Exception as e:
        print('Sender: An unexpected error occurred: {}'.format(e))
    

if __name__ == '__main__':
    main()








