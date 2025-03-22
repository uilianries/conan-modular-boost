#include <boost/tti/tti.hpp>
#include <iostream>

struct Test { typedef int value_type; };
BOOST_TTI_HAS_TYPE(value_type)

int main() {
    std::cout << "Boost TTI test package: " << std::boolalpha << has_type_value_type<Test>::value;
    return 0;
}