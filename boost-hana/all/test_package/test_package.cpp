#include <boost/hana.hpp>
#include <iostream>

int main() {
    auto tuple = boost::hana::make_tuple(42, "Boost HANA test package", 3.14);
    std::cout << boost::hana::at_c<1>(tuple) << std::endl;
    return 0;
}