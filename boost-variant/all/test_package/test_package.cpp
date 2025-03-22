#include <boost/variant.hpp>
#include <iostream>

int main() {
    boost::variant<int, std::string> v = "Boost Variant test package";
    std::cout << boost::get<std::string>(v) << std::endl;
    return 0;
}