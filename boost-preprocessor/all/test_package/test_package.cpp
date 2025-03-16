#include <boost/preprocessor.hpp>
#include <iostream>

int main() {
    std::cout << "Boost preprocessor: " << BOOST_PP_ADD(2,3) << std::endl;
    return 0;
}