#include <boost/convert.hpp>
#include <boost/convert/lexical_cast.hpp>
#include <iostream>

int main() {
    std::cout << "Boost Convert test package: " << boost::convert<int>("42", boost::cnv::lexical_cast()).value() << std::endl;
    return 0;
}