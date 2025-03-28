#include <boost/compute.hpp>
#include <iostream>

int main() {
    boost::compute::device device = boost::compute::system::default_device();
    std::cout << "Boost Compute test package: " << device.name() << std::endl;
    return 0;
}