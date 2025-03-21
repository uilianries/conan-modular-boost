#include <boost/static_string.hpp>
#include <iostream>

int main() {
    boost::static_string<16> str("Boost");
    std::cout << str << " Static String test package" << std::endl;
    return 0;
}