#include <boost/any.hpp>
#include <iostream>

int main() {
    boost::any a = 42;
    std::cout << "Boost Any test package: " << boost::any_cast<int>(a) << std::endl;
    return 0;
}