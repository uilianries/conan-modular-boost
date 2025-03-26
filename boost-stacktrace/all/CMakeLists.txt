cmake_minimum_required(VERSION 3.15)

if (BOOST_STACKTRACE_ENABLE_BACKTRACE)
    find_package(libbacktrace REQUIRED CONFIG)
    target_link_libraries(boost_stacktrace_backtrace PRIVATE libbacktrace::libbacktrace)
endif()
