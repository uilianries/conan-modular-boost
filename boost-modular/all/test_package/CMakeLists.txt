cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)

find_package(Boost REQUIRED CONFIG COMPONENTS regex log)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} Boost::regex Boost::log)
