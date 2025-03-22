#include <boost/regex.hpp>
#include <iostream>

int main() {
    boost::regex pat("([0-9]+)");
    std::cout << "Boost Regex test package: " << boost::regex_match("123", pat);
    return 0;
}