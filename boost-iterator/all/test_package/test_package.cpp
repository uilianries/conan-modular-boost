#include <boost/iterator/counting_iterator.hpp>
#include <iostream>

int main() {
    boost::counting_iterator<int> first(1), last(3);
    std::cout << "Boost Iterator test package: ";
    for (; first != last; ++first) std::cout << *first << ' ';
    std::cout << std::endl;
    return 0;
}