#include <boost/multiprecision/cpp_int.hpp>
#include <iostream>

int main() {
    boost::multiprecision::cpp_int big = 1;
    std::cout << "Boost Mutiprecision test package: " << (big << 1000) << std::endl;
    return 0;
}
