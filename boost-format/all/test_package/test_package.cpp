#include <boost/format.hpp>
#include <iostream>

int main() {
    std::cout << boost::format("Boost Format test package: %1%") % 42;
    return 0;
}