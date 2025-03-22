#include <boost/assign.hpp>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = boost::assign::list_of(1)(2)(3);
    std::cout << "Boost Assign test package: " << v[0] << std::endl;
    return 0;
}