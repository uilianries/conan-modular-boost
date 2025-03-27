cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)

find_package(boost_hana REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} Boost::hana)

# MSVC 192 fails to build with C++20:
# boost/hana/traits.hpp(74): error C2039: 'is_literal_type': is not a member of 'std'
# https://github.com/boostorg/hana/issues/516
target_compile_options(${PROJECT_NAME} PRIVATE $<$<CXX_COMPILER_ID:MSVC>:/Zc:__cplusplus>)
