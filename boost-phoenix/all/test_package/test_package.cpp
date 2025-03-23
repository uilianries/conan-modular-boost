#include <boost/phoenix.hpp>
#include <iostream>

int main() {
    std::cout << "Boost Phoenix test package: " << boost::phoenix::arg_names::arg1(42) << std::endl;
    return 0;
}
