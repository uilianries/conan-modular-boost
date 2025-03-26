cmake_minimum_required(VERSION 3.15)

find_package(boost_headers REQUIRED CONFIG)
find_package(boost_config REQUIRED CONFIG)
find_package(boost_assert REQUIRED CONFIG)
find_package(boost_core REQUIRED CONFIG)
find_package(boost_iterator REQUIRED CONFIG)
find_package(boost_utility REQUIRED CONFIG)
find_package(boost_predef REQUIRED CONFIG)
find_package(boost_thread REQUIRED CONFIG)

if (BOOST_LOCALE_ENABLE_ICU)
    find_package(ICU REQUIRED CONFIG)
endif()

if (BOOST_LOCALE_ENABLE_ICONV)
    find_package(Iconv REQUIRED CONFIG)
endif()
