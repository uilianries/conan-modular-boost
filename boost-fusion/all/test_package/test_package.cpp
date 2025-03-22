#include <boost/fusion/include/vector.hpp>
#include <boost/fusion/include/at_c.hpp>
#include <iostream>

int main() {
    boost::fusion::vector<int, std::string, double> v(1, "Boost Fusion test package", 3.14);
    std::cout << boost::fusion::at_c<1>(v) << std::endl;
    return 0;
}