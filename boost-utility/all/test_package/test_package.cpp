#include <boost/utility/base_from_member.hpp>
#include <iostream>

struct Base { Base(std::string x) { std::cout << "Boost Utility " << x << std::endl; } };

struct Derived : boost::base_from_member<std::string>, Base {
    Derived() : boost::base_from_member<std::string>("test package"),
     Base(base_from_member<std::string>::member) {}
};

int main() {
    Derived d;
    return 0;
}