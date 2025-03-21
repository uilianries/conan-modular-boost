#include <boost/safe_numerics/safe_integer.hpp>
#include <iostream>

int main() {
    boost::safe_numerics::safe<int> x = 100, y = 50;
    std::cout << "Boost Safe Numerics test package: " << x + y << std::endl;
    return 0;
}