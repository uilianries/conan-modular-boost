#include <boost/stl_interfaces/iterator_interface.hpp>
#include <iostream>

struct my_iterator :
    boost::stl_interfaces::iterator_interface<my_iterator, std::random_access_iterator_tag, int> {
        int* it; my_iterator(int* p) : it(p) {}
    };

int main() {
    std::cout << "Boost STL Interfaces test package: " << *my_iterator(new int(42)).it << std::endl;
    return 0;
}