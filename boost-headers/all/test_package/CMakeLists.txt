cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)

find_package(boost_headers REQUIRED CONFIG)
if (NOT TARGET Boost::headers)
    message(FATAL_ERROR "Boost::headers not found")
endif()
