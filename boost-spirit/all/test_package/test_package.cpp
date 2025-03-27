#include <boost/spirit/include/classic.hpp>
#include <boost/spirit/home/x3.hpp>
#include <iostream>

int main() {
    std::string str = "Hello";
    bool success = boost::spirit::x3::parse(str.begin(), str.end(), boost::spirit::x3::lit("Hello"));
    std::cout << "Boost Spirit test package: " << success << std::endl;
    return 0;
}