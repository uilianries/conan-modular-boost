#include <boost/container/vector.hpp>
#include <iostream>

int main() {
    boost::container::vector<int> vec = {1, 2, 3, 4, 5};
    std::cout << "Boost container vector size: " << vec.size() << std::endl;
    return 0;
}