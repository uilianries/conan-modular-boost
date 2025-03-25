cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)

find_package(boost_cobalt REQUIRED CONFIG)
find_package(boost_container REQUIRED CONFIG)
find_package(boost_context REQUIRED CONFIG)


add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} Boost::cobalt)
