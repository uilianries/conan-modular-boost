#include <boost/config.hpp>
#include <boost/version.hpp>
#include <iostream>

int main() {
    std::cout << "Boost version: " << BOOST_VERSION << std::endl;
    std::cout << "Boost library version: " << BOOST_LIB_VERSION << std::endl;
    return 0;
}
