#include <boost/ptr_container/ptr_vector.hpp>
#include <iostream>

int main() {
    boost::ptr_vector<int> vec;
    vec.push_back(new int(10));
    vec.push_back(new int(20));
    std::cout << "Boost Ptr Container test package: " << vec[0] << std::endl;
    return 0;
}