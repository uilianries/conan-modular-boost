#include <boost/numeric/conversion/cast.hpp>
#include <iostream>

int main() {
    std::cout << "Boost Numeric Conversion test package: " << boost::numeric_cast<int>(42.456) << std::endl;
    return 0;
}