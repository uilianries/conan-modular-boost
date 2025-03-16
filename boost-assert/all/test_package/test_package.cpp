#include <boost/assert.hpp>
#include <iostream>

int main() {
    int x = 1;
    BOOST_ASSERT(x == 1);
    BOOST_ASSERT_MSG(x > 0, "x must be positive");
    std::cout << "Boost assert test package" << std::endl;
    return 0;
}