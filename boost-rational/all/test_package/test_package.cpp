#include <boost/rational.hpp>
#include <iostream>

int main() {
    boost::rational<int> r1(1, 2), r2(1, 3);
    std::cout << "Boost Ration test package: " << r1 + r2 << std::endl;
    return 0;
}