#include <boost/xpressive/xpressive.hpp>
#include <iostream>

int main() {
    std::string str = "Boost Xpressive world";
    boost::xpressive::sregex rex = boost::xpressive::sregex::compile("world");
    std::cout << boost::xpressive::regex_replace(str, rex, "test package") << std::endl;
    return 0;
}