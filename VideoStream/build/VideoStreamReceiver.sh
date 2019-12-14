#!/bin/bash
export ADLINK_DATARIVER_URI=file://$EDGE_SDK_HOME/etc/config/default_datariver_config_v1.2.xml

THING_PROPERTIES_URI=file://./config/VideoStreamReceiverProperties.json
RUNNING_TIME=${1:-60}

./VideoStreamReceiver $THING_PROPERTIES_URI $RUNNING_TIME
