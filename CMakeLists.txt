cmake_minimum_required(VERSION 3.10)
project(camera-calibration CXX C)
set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_compile_options($<$<COMPILE_LANGUAGE:CXX>:-Werror>)

#set(OpenCV_DIR "/usr/local/opencv-4.6.0") # Only valid on jetson board with opencv
find_package(OpenCV)
find_package(OpenCV REQUIRED COMPONENTS aruco core) # QUIET)


#add_executable(camcalib camera_calibration.cpp)
add_executable(camcalib camera_calibration_v4_11_0.cpp)

target_link_libraries(camcalib ${OpenCV_LIBS})
