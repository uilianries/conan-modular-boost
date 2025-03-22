#include <boost/algorithm/string.hpp>
#include <boost/algorithm/algorithm.hpp>
#include <iostream>

int main() {
    std::string str1 = "Boost";
    std::string str2 = "boost";
    if (boost::iequals(str1, str2)) {
        std::cout << "Boost Algorithm test package" << std::endl;
    }
    return 0;
}