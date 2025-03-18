#include <boost/dynamic_bitset.hpp>
#include <iostream>

int main() {
    boost::dynamic_bitset<> bits(8, 170);
    std::cout << "Boost Dymanic Bitset test package: " << bits << std::endl;
    return 0;
}