#include <boost/core/ignore_unused.hpp>
#include <boost/core/lightweight_test.hpp>
#include <iostream>

int main() {
    int x = 42; boost::ignore_unused(x);
    BOOST_TEST(true);
    std::cout << "Boost Core test package: ";
    boost::report_errors();
    return 0;
}