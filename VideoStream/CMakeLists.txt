project( VideoStream )
cmake_minimum_required(VERSION 3.5)

# make sure we can find the ThingAPI package...
if(NOT TARGET ThingAPI::ThingAPI)
	if("$ENV{EDGE_SDK_HOME}" STREQUAL "")
	    message(FATAL_ERROR "Environment variable EDGE_SDK_HOME is not set. Please run config_env_variables.com/bat script to set the environment variables")
	endif()

    file(TO_CMAKE_PATH "$ENV{EDGE_SDK_HOME}" EDGE_SDK_HOME_PATH)
	list(APPEND CMAKE_MODULE_PATH "${EDGE_SDK_HOME_PATH}/cmake")

	find_package(ThingAPI REQUIRED)
	find_package( OpenCV REQUIRED )
endif()

include_directories( ${OpenCV_INCLUDE_DIRS} )

add_executable( VideoStreamSender src/VideoStreamSender.cpp )

target_link_libraries( VideoStreamSender ${OpenCV_LIBS} )
target_link_libraries( VideoStreamSender ThingAPI::ThingAPI )

set_property(TARGET VideoStreamSender PROPERTY CXX_STANDARD 11)
set_property(TARGET VideoStreamSender PROPERTY OUTPUT_NAME "VideoStreamSender")

file(COPY definitions DESTINATION .)
file(COPY config DESTINATION .)

configure_file(VideoStreamSender.sh VideoStreamSender.sh COPYONLY)
