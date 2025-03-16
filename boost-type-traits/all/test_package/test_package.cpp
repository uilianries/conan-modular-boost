#include <boost/type_traits.hpp>
#include <iostream>


int main() {
    std::cout << "Boost Type Traits test package: " << std::boolalpha << boost::is_pointer<int*>::value << std::endl;
    return 0;
}