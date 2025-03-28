cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)

find_package(boost_parameter_python REQUIRED CONFIG)
find_package(Python COMPONENTS Development REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE Boost::parameter_python Python::Python)
