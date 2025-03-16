#include <boost/array.hpp>
#include <iostream>

int main() {
    boost::array<int, 3> arr = {1, 2, 3};
    std::cout << "Boost Array test package: " << arr.size() << std::endl;
    return 0;
}