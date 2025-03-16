#include <boost/ratio.hpp>
#include <iostream>

int main() {
    std::cout << "Boost Ratio test package: " << boost::ratio<42, 4>::num << std::endl;
    return 0;
}