#include <boost/parser/parser.hpp>
#include <iostream>

int main() {
    auto result = boost::parser::parse("123", boost::parser::char_);
    std::cout << "Boost Parser test package: " << *result << std::endl;
    return 0;
}