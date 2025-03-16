#include <boost/move/utility_core.hpp>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v1{1, 2, 3};
    std::vector<int> v2(boost::move(v1));
    std::cout << "Boost move test package: " << v1.size() << std::endl;
    return 0;
}