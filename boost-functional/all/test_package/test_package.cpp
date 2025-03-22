#include <boost/function.hpp>
#include <iostream>

void print_message() { std::cout << "Boost Functional test package" << std::endl; }

int main() {
    boost::function<void()> func = print_message;
    func();
    return 0;
}