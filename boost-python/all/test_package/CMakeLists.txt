cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)

find_package(boost_python REQUIRED CONFIG)
find_package(Python COMPONENTS Development REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} Python::Python Boost::python $<$<TARGET_EXISTS:Boost::numpy>:Boost::numpy>)
