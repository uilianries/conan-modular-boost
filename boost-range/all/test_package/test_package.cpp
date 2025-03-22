#include <boost/range/algorithm.hpp>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {3, 1, 4, 1, 5};
    boost::sort(v);
    std::cout << "Boost Range test package: " << v[0] << std::endl;
    return 0;
}