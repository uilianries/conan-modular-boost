#include <boost/vmd/is_empty.hpp>
#include <iostream>

#define NON_EMPTY_MACRO something

int main() {
    std::cout << "Boost VMD test package: " << BOOST_VMD_IS_EMPTY(NON_EMPTY_MACRO) << std::endl;
    return 0;
}