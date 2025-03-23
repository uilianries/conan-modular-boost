#define BOOST_TEST_MODULE Minimal
#include <boost/test/included/unit_test.hpp>
#include <iostream>

BOOST_AUTO_TEST_CASE(minimal_test) {
    std::cout << "Boost Test test package" << std::endl;
    BOOST_TEST(true);
}
