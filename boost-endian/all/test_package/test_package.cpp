#include <boost/endian/conversion.hpp>
#include <iostream>

int main() {
    uint32_t x = 0x12345678;
    uint32_t y = boost::endian::endian_reverse(x);
    std::cout << "Boost endian test package: " << std::hex << y << std::endl;
    return 0;
}