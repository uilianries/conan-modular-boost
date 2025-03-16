#include <boost/bind/bind.hpp>
#include <iostream>

void print(int x) { std::cout << "Boost Bind test package: " << x << std::endl; }

int main() {
    boost::bind(print, 42)();
    return 0;
}