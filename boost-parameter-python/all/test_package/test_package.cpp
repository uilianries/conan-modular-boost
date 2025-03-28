#include <boost/parameter/keyword.hpp>
#include <iostream>

BOOST_PARAMETER_KEYWORD(tags, x)
BOOST_PARAMETER_KEYWORD(tags, y)

int main() {
    std::cout << "Boost Parameter Python test package" << std::endl;
    return 0;
}
