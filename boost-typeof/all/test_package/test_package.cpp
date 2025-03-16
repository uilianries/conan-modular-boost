#include <boost/typeof/typeof.hpp>
#include <iostream>

int main() {
    BOOST_TYPEOF(3.14) pi = 3.14;
    std::cout << "Boost typeof test package: " << pi << std::endl;
    return 0;
}