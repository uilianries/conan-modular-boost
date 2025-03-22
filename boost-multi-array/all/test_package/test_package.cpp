#include <boost/multi_array.hpp>
#include <iostream>

int main() {
    boost::multi_array<int, 2> array(boost::extents[3][4]);
    array[1][2] = 42;
    std::cout << "Boost Multi Array test package: " << array[1][2] << std::endl;
    return 0;
}