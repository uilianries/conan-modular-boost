#include <boost/variant2/variant.hpp>
#include <iostream>

int main() {
    boost::variant2::variant<int, float> v{42};
    std::cout << "Boost Variant2 test package: " << boost::variant2::get<0>(v) << std::endl;
    return 0;
}