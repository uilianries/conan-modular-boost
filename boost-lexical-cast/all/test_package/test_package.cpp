#include <boost/lexical_cast.hpp>
#include <iostream>
int main() {
    std::string number = boost::lexical_cast<std::string>(42.123);
    std::cout << "Boost Lexical Cast test package: " << number << std::endl;
    return 0;
}