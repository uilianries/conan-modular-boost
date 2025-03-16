#include <boost/static_assert.hpp>
#include <type_traits>
#include <iostream>

int main() {
    BOOST_STATIC_ASSERT(10 >= 4);
    std::cout << "Boost static assert test package" << std::endl;
    return 0;
}