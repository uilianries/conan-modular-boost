#include <boost/integer.hpp>
#include <iostream>

int main() {
    boost::int_t<32>::exact x = 42;
    std::cout << "Boost Integer test package: " << x << std::endl;
    return 0;
}