#include <boost/sort/spreadsort/float_sort.hpp>
#include <vector>
#include <iostream>
int main() {
    std::vector<float> v = {3.14f, 1.41f, 2.71f};
    boost::sort::spreadsort::float_sort(v.begin(), v.end());
    std::cout << "Boost Sort test package: " << v[0] << std::endl;
    return 0;
}