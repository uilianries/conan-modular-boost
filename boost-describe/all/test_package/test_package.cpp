#include <boost/describe.hpp>
#include <iostream>

BOOST_DEFINE_ENUM(Color, red, green, blue)

int main() {
    Color c = Color::red;
    std::cout << "Boost Describe test package: " << boost::describe::enum_to_string(c, "unknown") << std::endl;
    return 0;
}