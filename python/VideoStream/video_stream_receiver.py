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
import os
import time
import sys
from adlinktech.datariver import DataRiver, JSonTagGroupRegistry, JSonThingClassRegistry, JSonThingProperties, FlowState
import cv2
import numpy as np

try:
    from openvino import inference_engine as ie
    from openvino.inference_engine import IENetwork, IEPlugin
except Exception as e:
    exception_type = type(e).__name__
    print("The following error happened while importing Python API module: \n[ {} ] {}".format(exception_type, e))
    sys.exit(1)

def load_model():
    plugin_dir = None
    model_xml = "handwritten.xml"
    model_bin = "handwritten.bin"
    print("Loading network files:\n\t{}\n\t{}".format(model_xml, model_bin))

    plugin = IEPlugin("MYRIAD", plugin_dirs=plugin_dir)

    net = IENetwork(model=model_xml, weights=model_bin)

    assert len(net.inputs.keys()) == 1
    assert len(net.outputs) == 1

    return plugin, net

'''
Returns an absolute file uri of a given relative file path.
Allows to run this example from any location
'''
def get_abs_file_uri(filepath):
    dirpath = os.path.dirname(os.path.abspath(__file__))
    return 'file://' + str(os.path.join(dirpath, filepath))

class VideoStreamReceiver(object):
    
    # Initializing
    def __init__(self, thing_properties_uri):
        self._thing_properties_uri = thing_properties_uri
        
        self._dr = None
        self._thing = None
        self._frame = np.empty([7, 10, 3])
        self._temp = np.empty([210])
    # Enter the runtime context related to the object
    def __enter__(self):
        self._dr = DataRiver.get_instance()
        self._thing = self.create_thing()
        
        print('Video Stream receiver started')
        
        return self
    
    # Exit the runtime context related to the object
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._dr is not None:
            self._dr.close()
        print('Video Stream receiver stopped')
        
    def create_thing(self):
        # Create and Populate the TagGroup registry with JSON resource files.
        tgr = JSonTagGroupRegistry()
        tgr.register_tag_groups_from_uri(get_abs_file_uri('definitions/TagGroup/com.adlinktech.MQ/VideoStreamTagGroup.json'))
        self._dr.add_tag_group_registry(tgr) 
 
        # Create and Populate the ThingClass registry with JSON resource files.
        tcr = JSonThingClassRegistry()
        tcr.register_thing_classes_from_uri(get_abs_file_uri('definitions/ThingClass/com.adlinktech.MQ/VideoStreamReceiverThingClass.json'))
        self._dr.add_thing_class_registry(tcr)
 
        # Create a Thing based on properties specified in a JSON resource file.
        tp = JSonThingProperties()
        tp.read_properties_from_uri(self._thing_properties_uri)
        return self._dr.create_thing(tp)
    
    def run(self, running_time) :
        start = time.time()
        elapsed_seconds = 0
        print("Handwritten Digits Prediction")

        #log.basicConfig(format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout)

        plugin, net = load_model()

        input_blob = next(iter(net.inputs))
        output_blob = next(iter(net.outputs))
        print("Loading IR to the plugin...")

        exec_net = plugin.load(network=net)

        print("Input shapes: " + str(net.inputs[input_blob].shape))
        print("Output shapes: " + str(net.outputs[output_blob].shape))
        del net

        print("Starting inference...")

        while True:
            # Read all data for input 'temperature'
            msgs = self._thing.read_iot_nvp('video', int((running_time - elapsed_seconds) * 1000))
            
            for msg in msgs:
                flow_state = msg.flow_state
                if flow_state == FlowState.ALIVE:
                    #data_sample = msg.data
                    received_data = 0
                    
                    try:
                        for nvp in msg.data:
                            if nvp.name == 'video':
                                received_data = nvp.value.byte_seq
                                #temp = np.empty([1, 307200], dtype=np.uint8)
                                
                                #temp = np.copy(received_data)
                                #print(type(temp))
                                #print(received_data.shape)
                                #print(temp)
                                temp = []
                                temp.extend(nvp.value.byte_seq)
                                #print(type(temp[0]))
                                #for i in received_data:
                                    #print(i)
                                    #temp.append(np.uint8(i))
                                #print(newArr)
                                #print("---")
                    except Exception as e:
                        print('An unexpected error occured while processing data-sample ' + str(e))
                        continue
                    
                    #print('Video data received: {}'.format(temperature[0]))
                    #A = np.arange(210)
                    display_frame = np.reshape(temp, (480, 640, 1))
                    display_frame = display_frame.astype('uint8')
                    #frame = np.reshape(temp,(150, 200, 1))
                    #newArr = np.reshape(temperature,(7, 10, 3))
                    #self._frame = temperature.reshape((7, 10, 3)).transpose()
                    #print(B)
                    #print(frame)
                    #print(frame.shape)
                    #cv2.imshow('Frame',frame)

                    frame = cv2.resize(display_frame, (28, 28))
                    frame = np.reshape(frame, [1, 1, 28, 28])
                    #print(frame.shape)
                    #frame = frame.astype('float32')
                    #frame = frame / 255.0

                    res = exec_net.infer(inputs={input_blob:frame})
                    output_node_name = list(res.keys())[0]
                    #res = exec_net.requests[0].outputs[output_blob]
                    #res = exec_net.requests[0].get_perf_counts()
                    res = res[output_node_name]
                    idx = np.argsort(res[0])[-1]
                    #print("- Detected #: " + str(idx))
                    
                    cv2.putText(display_frame, "Detected #: " + str(idx), (20, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    cv2.imshow("Image", display_frame)

            key = cv2.waitKey(5)
            if key == 27:
                break



            # Wait for some time before reading next samples
            #time.sleep(READ_SAMPLE_DELAY)

            # Press Q on keyboard to  exit
            #if cv2.waitKey(25) & 0xFF == ord('q'):
                #break

            elapsed_seconds = time.time() - start
            
            #if elapsed_seconds >= float(running_time):
                #break
        cv2.destroyAllWindows()
        del exec_net
        del plugin

def main():
    # Get thing properties URI from command line parameter
    parser = argparse.ArgumentParser()
    parser.add_argument('running_time', type=int, nargs='?',
                        help='Total running time of the program (in seconds)',
                        default=60)
    parser.add_argument('thing_properties_uri', type=str, nargs='?',
                        help='URI of the thing properties file',
                        default='file://./config/VideoStreamReceiverProperties.json')
    args = parser.parse_args()
    
    try:
        temp_display = VideoStreamReceiver(args.thing_properties_uri)
        # The 'with' statement supports a runtime context which is implemented
        # through a pair of methods executed (1) before the statement body is 
        # entered (__enter__()) and (2) after the statement body is exited (__exit__())
        with temp_display as tdisplay:
            tdisplay.run(args.running_time)
    except Exception as e:
        print('Display: An unexpected error occurred: {}'.format(e))
    

if __name__ == '__main__':
    main()
