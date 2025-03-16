#include <boost/circular_buffer.hpp>
#include <iostream>

int main() {
    boost::circular_buffer<int> buffer(3);
    std::cout << "Boost Circular Buffer test package: " << buffer.size() << std::endl;
    return 0;
}